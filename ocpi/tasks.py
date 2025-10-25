from ocpi.models import Cdr
from transaction.models import Transaction
from ocpi.classes import AuthMethod, Price, ChargingPeriod, CdrDimension, CdrDimensionType
import logging
from celery import shared_task
from ov2xmp.helpers import convert_special_types
from users.models import User, Profile
from sampledvalue.models import Sampledvalue
import datetime
import zoneinfo


ov2xmp_logger = logging.getLogger('ov2xmp')
ov2xmp_logger.setLevel(logging.DEBUG)


@shared_task()
def create_cdr(transaction_id):

    if type(transaction_id) is int:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    else:
        transaction = Transaction.objects.get(uuid=transaction_id)
        
    ov2xmp_logger.info({"message": "Creating CDR for <transaction_id: " + str(transaction_id) + ">"})

    if transaction.connector is not None:
        
        # If there are tariffs associated with the connector
        if transaction.connector.tariff_ids.count() > 0:

            ov2xmp_logger.info({"message": "Tariffs exist - Proceeding to CDR creation for <transaction_id: " + str(transaction_id) + ">"})
            
            chargingperiods = []

            total_fixed_cost_exclVat = 0.0
            total_fixed_cost_vatOnly = 0.0

            # At the moment, we do not charge parking time, because we cannot know for how long the user parked their EV.
            total_parking_time = 0.0
            total_parking_cost = Price(excl_vat=0.0, incl_vat=0.0)

            # At the moment, we do not charge reservations. TODO: Implement the ability to calculate reservation cost, check 11.4.5 section of OCPI 2.2.1
            total_reservation_cost = Price(excl_vat=0.0, incl_vat=0.0)

            # At the moment, we do not charge based on how long the user used the EV charger
            total_time_cost = Price(excl_vat=0.0, incl_vat=0.0)

            # Calculate total energy consumed in kW
            total_energy = 0
            
            # Initialize the total_energy_cost variables
            total_energy_cost_vatOnly = 0.0
            total_energy_cost_exclVat = 0.0

            # Calculate total duration of the session in hours
            total_time = (transaction.wh_meter_last_timestamp - transaction.start_transaction_timestamp).total_seconds()/3600.0

            # Calculate the deltas (i.e., differences between consequent samplevalues that are chargable). For each delta, we need to find later the appropriate TariffElement to apply.
            samplevalues = Sampledvalue.objects.filter(
                transaction = transaction,
                measurand = "Energy.Active.Import.Register",
                unit = 'Wh'
            ).order_by('timestamp')
            samplevalues = list(samplevalues)
            deltas = []
            for i in range(1, len(samplevalues)):
                deltas.append({
                    "start_time": samplevalues[i-1].timestamp,
                    "end_time": samplevalues[i].timestamp,
                    "value": abs(int(samplevalues[i].value) - int(samplevalues[i-1].value))*0.001  # Convert each delta to kwh
                })
            
            # Find tariffs that cover the transaction
            connector_tariffs = transaction.connector.tariff_ids.all()
            applicable_tariffs_for_transaction = []
            for _tariff in connector_tariffs:
                if (_tariff.start_date_time <= samplevalues[0].timestamp and _tariff.end_date_time >= samplevalues[-1].timestamp) or \
                   (_tariff.start_date_time >= samplevalues[0].timestamp and _tariff.end_date_time <= samplevalues[-1].timestamp) or \
                   (_tariff.start_date_time >= samplevalues[0].timestamp and _tariff.end_date_time >= samplevalues[-1].timestamp):
                    applicable_tariffs_for_transaction.append(_tariff)

            # For each delta, select the applicable tariff. 
            # For the applicable tariff, go through the TariffElements and if there are restrictions, apply the first TariffElement that falls .TODO: Consider more possible restrictions.
            for delta in deltas:
                applicable_tariffs_for_delta = []
                for _tariff in applicable_tariffs_for_transaction:
                    if (_tariff.start_date_time <= delta["start_time"] and _tariff.end_date_time >= delta["end_time"]) or \
                       (_tariff.start_date_time >= delta["start_time"] and _tariff.end_date_time <= delta["end_time"]) or \
                       (_tariff.start_date_time >= delta["start_time"] and _tariff.end_date_time >= delta["end_time"]):
                        applicable_tariffs_for_delta.append(_tariff)
                    
                # If multiple tariffs overlap during the delta, get the tariff that was most recently updated (the newest)
                if len(applicable_tariffs_for_delta) > 1:
                    single_applicable_tariff = sorted(applicable_tariffs_for_delta, key=lambda x: x.last_updated, reverse=True)[0]
                elif len(applicable_tariffs_for_delta) == 1:
                    single_applicable_tariff = applicable_tariffs_for_delta[0]
                else: # TODO: What happens if there is no tariff?
                    ov2xmp_logger.warning({"message": "No applicable tariff for delta: <start_time: " + str(delta["start_time"]) + ", end_time: " + str(delta["end_time"]) + ", value: " + str(delta["value"]) + ">"})
                    continue
                
                # The applicable tariff has been found, now go through the TariffElements and find the one that applies
                for _element in single_applicable_tariff.elements.all():
                    
                    # If there are restrictions of start_date and end_date, we should check 
                    if 'start_date' in _element.restrictions and 'end_date' in _element.restrictions:
                        # Restriction - start_date in UTC
                        restriction_start_datetime_utc = datetime.datetime.strptime(_element.restrictions["start_date"] + ' ' + _element.restrictions["start_time"], '%Y-%m-%d %H:%M:%S').replace(tzinfo=zoneinfo.ZoneInfo('Europe/Athens')).astimezone(tz=datetime.timezone.utc)
                        # Restriction - end_time in UTC
                        restriction_end_datetime_utc = datetime.datetime.strptime(_element.restrictions["end_date"] + ' ' + _element.restrictions["end_time"], '%Y-%m-%d %H:%M:%S').replace(tzinfo=zoneinfo.ZoneInfo('Europe/Athens')).astimezone(tz=datetime.timezone.utc)

                        # If there are restrictions, but they do not fall inside the delta duration, then continue with the next element of the tariff
                        if not ((restriction_start_datetime_utc <= delta["start_time"] and restriction_end_datetime_utc >= delta["end_time"]) or \
                           (restriction_start_datetime_utc >= delta["start_time"] and restriction_end_datetime_utc <= delta["end_time"]) or \
                           (restriction_start_datetime_utc >= delta["start_time"] and restriction_end_datetime_utc >= delta["end_time"])): 
                            continue

                    # Arriving here means that the current tariff element applies to the current delta 
                    # We always expect only one ENERGY price component. We calculate energy cost only when there is an ENERGY price component
                    for _priceComponent in _element.price_components:
                        if _priceComponent["type"] == "ENERGY":
                            # We will create a chargingPeriod for the delta
                            chargingperiods.append(
                                ChargingPeriod(
                                    start_date_time = delta["start_time"].isoformat(), 
                                    dimensions = CdrDimension(
                                        type=CdrDimensionType.ENERGY,
                                        volume=delta["value"]
                                    ),
                                    tariff_id = str(single_applicable_tariff.id)
                                )
                            )
                            # Calculate the delta cost                            
                            # duration of the delta in hours
                            total_energy += delta["value"]
                            cost_kwh = delta["value"] * _priceComponent["price"]
                            # Add the delta cost to the total energy cost
                            # NOTE: The calculated cost is assumed that is always without VAT
                            total_energy_cost_exclVat += cost_kwh
                            total_energy_cost_vatOnly += cost_kwh*(_priceComponent["vat"]/100.0)
                            break # Dont look for other price_components, only ENERGY we were looking for
                    
                    # Arriving here means that we applied a tariff-element for our delta. So, we stop looking for the other tariff-elements, and check for the next delta
                    break

            total_energy_cost = Price(excl_vat=total_energy_cost_exclVat, incl_vat=total_energy_cost_exclVat+total_energy_cost_vatOnly)
            total_fixed_cost = Price(excl_vat=total_fixed_cost_exclVat, incl_vat=total_fixed_cost_exclVat+total_fixed_cost_vatOnly)

            total_cost = Price(excl_vat=total_energy_cost_exclVat+total_fixed_cost_exclVat, incl_vat=total_energy_cost_exclVat+total_energy_cost_vatOnly+total_fixed_cost_exclVat+total_fixed_cost_vatOnly)

            cdr = Cdr(
                start_date_time = transaction.start_transaction_timestamp,
                end_date_time = transaction.stop_transaction_timestamp,
                session_id = transaction,
                cdr_token = transaction.id_tag,
                auth_method = AuthMethod.COMMAND.value,
                cdr_location = transaction.connector.chargepoint.location,
                tariffs = transaction.tariffs,
                charging_periods = convert_special_types(chargingperiods),
                total_cost = convert_special_types(total_cost),
                total_fixed_cost = convert_special_types(total_fixed_cost),
                total_energy = total_energy,
                total_energy_cost = convert_special_types(total_energy_cost),
                total_time = total_time,
                total_time_cost = convert_special_types(total_time_cost),
                total_parking_time = total_parking_time,
                total_parking_cost = convert_special_types(total_parking_cost),
                total_reservation_cost = convert_special_types(total_reservation_cost),
                home_charging_compensation = False
            )

            cdr.save()

            msg = {"success": True, "message": "A new CDR has been created", "cdr_id": cdr.id, "transaction_id": transaction_id}

            return(msg, cdr)
        
        else:
            msg = {"success": False, "message": "No CDR was created because no tariffs are associated with the connector.", "cdr_id": None, "transaction_id": None}
            
    else:
        msg = {"success": False, "message": "No CDR was created because no connector is associated with the transaction.", "cdr_id": None, "transaction_id": None}

    return (msg, None)


@shared_task()
def apply_cdr(cdr: Cdr, user:User):
    
    user_profile = Profile.objects.get(user=user)

    old_balance = user_profile.credit_balance
    new_balance = old_balance - cdr.total_cost["incl_vat"]
    user_profile.credit_balance = new_balance

    user_profile.save()

    ov2xmp_logger.info("Balance updated for <user: " + user.username + "> after applying <CDR: " + str(cdr.id) + ">. Old balance: " + str(old_balance) + ". New balance: " + str(new_balance))

    return True
