import os
import json
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from dso_rest.models import DsoSignal

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import DSO signals from JSON archive files back into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Specific JSON file to import (e.g., dso_signals_20_01_1970.json)',
        )
        parser.add_argument(
            '--path',
            type=str,
            default=None,
            help='Path to the archive directory (default: dso_rest/dso_archive)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Import all JSON files from the archive directory',
        )

    def handle(self, *args, **options):
        # Set default archive path if not provided
        archive_path = options['path']
        if not archive_path:
            archive_path = os.path.join(settings.BASE_DIR, 'dso_rest', 'dso_archive')

        if not os.path.exists(archive_path):
            self.stdout.write(self.style.ERROR(f'Archive path does not exist: {archive_path}'))
            return

        # Determine which files to import
        files_to_import = []
        
        if options['file']:
            # Import specific file
            filepath = os.path.join(archive_path, options['file'])
            if os.path.exists(filepath):
                files_to_import.append(filepath)
            else:
                self.stdout.write(self.style.ERROR(f'File not found: {filepath}'))
                return
        elif options['all']:
            # Import all JSON files in directory
            for filename in os.listdir(archive_path):
                if filename.endswith('.json') and filename.startswith('dso_signals_'):
                    files_to_import.append(os.path.join(archive_path, filename))
        else:
            self.stdout.write(self.style.ERROR('Please specify either --file or --all'))
            return

        if not files_to_import:
            self.stdout.write(self.style.WARNING('No files to import'))
            return

        # Process each file
        total_imported = 0
        total_skipped = 0
        total_errors = 0

        for filepath in files_to_import:
            filename = os.path.basename(filepath)
            self.stdout.write(f'\nProcessing file: {filename}')
            
            imported, skipped, errors = self.import_file(filepath)
            total_imported += imported
            total_skipped += skipped
            total_errors += errors

        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n=== Import Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Total signals imported: {total_imported}'))
        if total_skipped > 0:
            self.stdout.write(self.style.WARNING(f'Total signals skipped (already exist): {total_skipped}'))
        if total_errors > 0:
            self.stdout.write(self.style.ERROR(f'Total errors: {total_errors}'))

    def import_file(self, filepath):
        """Import DSO signals from a single JSON file"""
        imported_count = 0
        skipped_count = 0
        error_count = 0

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                signals_data = json.load(f)

            self.stdout.write(f'Found {len(signals_data)} signals in file')

            for signal_data in signals_data:
                try:
                    signal_id = signal_data.get('id')
                    
                    # Check if signal already exists
                    if DsoSignal.objects.filter(id=signal_id).exists():
                        self.stdout.write(self.style.WARNING(f'  Signal {signal_id} already exists, skipping'))
                        skipped_count += 1
                        continue

                    # Create the DSO signal
                    DsoSignal.objects.create(
                        id=signal_data['id'],
                        uuId=signal_data['uuId'],
                        uuName=signal_data['uuName'],
                        event_timestamp=signal_data['event_timestamp'],
                        locationCoords=signal_data['locationCoords'],
                        locationName=signal_data['locationName'],
                        transformerID=signal_data['transformerID'],
                        duration=signal_data['duration'],
                        period=signal_data['period']
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Imported signal {signal_id}'))
                    imported_count += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error importing signal {signal_id}: {str(e)}'))
                    error_count += 1
                    continue

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file {filepath}: {str(e)}'))
            return 0, 0, 1

        return imported_count, skipped_count, error_count