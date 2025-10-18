# Save this as: connector/management/commands/migrate_to_5min_intervals.py

from django.core.management.base import BaseCommand
from connector.helpers import reinitialize_all_connectors, test_update_logic
import logging

logger = logging.getLogger('ov2xmp')

class Command(BaseCommand):
    help = 'Migrate all connectors from 30-minute to 5-minute time intervals'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run in dry-run mode without making changes',
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Run test logic to verify the update functionality',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting migration to 5-minute intervals...')
        )

        if options['test']:
            self.stdout.write("Running test logic...")
            success = test_update_logic()
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✓ Test completed successfully')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('✗ Test failed')
                )
            return

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
            # Here you could add logic to show what would be changed
            from connector.models import Connector
            
            total_connectors = Connector.objects.count()
            connectors_to_update = 0
            
            for connector in Connector.objects.all():
                tariff_slots = len(connector.tariff_history) if connector.tariff_history else 0
                capacity_slots = len(connector.capacity_history) if connector.capacity_history else 0
                
                if tariff_slots != 288 or capacity_slots != 288:
                    connectors_to_update += 1
                    self.stdout.write(
                        f"Would update {connector.uuid}: "
                        f"tariff_slots={tariff_slots}, capacity_slots={capacity_slots}"
                    )
            
            self.stdout.write(
                f"Would update {connectors_to_update} out of {total_connectors} connectors"
            )
            return

        # Actual migration
        try:
            updated_count = reinitialize_all_connectors()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {updated_count} connectors to 5-minute intervals'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Migration failed: {str(e)}')
            )
            raise