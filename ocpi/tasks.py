from ocpi.models import Cdr
from transaction.models import Transaction
from ocpi.classes import AuthMethod, Price, ChargingPeriod, CdrDimension, CdrDimensionType
import logging
from celery import shared_task
from api.serializers import CSMS_MESSAGE_CODE
from api.helpers import convert_special_types
from users.models import User, Profile

ov2xmp_logger = logging.getLogger('ov2xmp')
ov2xmp_logger.setLevel(logging.DEBUG)


@shared_task()
def create_cdr(transaction_id):

    transaction = Transaction.objects.get(transaction_id=transaction_id)
    ov2xmp_logger.info({"message": "Creating CDR for <transaction_id: " + str(transaction_id) + ">"})

    if transaction.connector is not None and transaction.tariffs is not None:
        if transaction.tariffs.__len__() > 0:

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
            if transaction.wh_meter_stop is None:
                total_energy = (transaction.wh_meter_last - transaction.wh_meter_start)*0.001
            else:
                total_energy = (transaction.wh_meter_stop - transaction.wh_meter_start)*0.001

            total_energy_cost_vatOnly = 0.0
            total_energy_cost_exclVat = 0.0

            # Calculate total duration of the session in hours
            total_time = (transaction.wh_meter_last_timestamp - transaction.start_transaction_timestamp).total_seconds()/3600.0

            for _tariff in transaction.tariffs:
                # TODO: restrictions are not considered
                for _element in _tariff["elements"]:
                    for _priceComponent in _element["price_components"]:

                        if _priceComponent["type"] == "FLAT":
                            # Add the flat cost and its VAT to the total fixed cost
                            total_fixed_cost_exclVat += _priceComponent["price"]
                            total_fixed_cost_vatOnly += _priceComponent["price"]*(_priceComponent["vat"]/100.0)

                        elif _priceComponent["type"] == "ENERGY":
                            # Create a chargingperiod that corresponds to the consumed energy of the transaction
                            # TODO: Instead of setting the total_energy as volume, we should calculate how much energy was consumed during the tariff (end_date_time - start_date_time). Now, we just assume that the tariff was applied during the whole duration of the transaction.
                            # At this moment, ONLY ONE tariff should be associated with the transaction, because otherwise the backend will apply the same tariff multiple times for the same Wh.
                            consumed_energy = total_energy

                            chargingperiods.append(
                                ChargingPeriod(
                                    start_date_time = transaction.start_transaction_timestamp.isoformat(), 
                                    dimensions = CdrDimension(
                                        type=CdrDimensionType.ENERGY,
                                        volume=consumed_energy
                                    ),
                                    tariff_id = _tariff["id"]
                                )
                            )

                            # We calculate energy cost only when there is an ENERGY price component
                            cost_kwh = consumed_energy * total_time * _priceComponent["price"]
                            total_energy_cost_exclVat += cost_kwh
                            total_energy_cost_vatOnly += cost_kwh*(_priceComponent["vat"]/100.0)

                        # Ignore TIME pricecomponent
                        # Ignore PARKING_TIME pricecomponent
            
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

            return({"success": True, "message": "A new CDR has been created", "cdr_id": cdr.id, "transaction_id": transaction_id}, cdr)

@shared_task()
def apply_cdr(cdr: Cdr, user:User):
    
    user_profile = Profile.objects.get(user=user)

    old_balance = user_profile.credit_balance
    new_balance = old_balance - cdr.total_cost["incl_vat"]
    user_profile.credit_balance = new_balance

    user_profile.save()

    ov2xmp_logger.info("Balance updated for <user: " + user.username + "> after applying <CDR: " + str(cdr.id) + ">. Old balance: " + str(old_balance) + ". New balance: " + str(new_balance))

    return True
    



