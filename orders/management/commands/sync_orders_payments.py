"""
Commande Django pour synchroniser les statuts entre Order et Payment
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from orders.models import Order
from orders.sync_utils import get_status_consistency_report, sync_order_payment_status


class Command(BaseCommand):
    help = 'Synchronise les statuts entre les commandes et les paiements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les incohérences sans les corriger',
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Corrige automatiquement les incohérences',
        )
        parser.add_argument(
            '--order-id',
            type=int,
            help='Synchronise une commande spécifique',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fix = options['fix']
        order_id = options.get('order_id')

        if order_id:
            # Synchroniser une commande spécifique
            self.sync_single_order(order_id, dry_run)
        else:
            # Générer un rapport des incohérences
            self.generate_report(dry_run, fix)

    def sync_single_order(self, order_id, dry_run):
        """Synchronise une commande spécifique"""
        try:
            order = Order.objects.get(id=order_id)
            self.stdout.write(f"Synchronisation de la commande {order.order_number} (ID: {order_id})")
            
            if dry_run:
                self.stdout.write(self.style.WARNING("Mode dry-run: aucune modification effectuée"))
                return
            
            # Synchroniser le statut de paiement
            success = sync_order_payment_status(order, order.payment_status)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Commande {order.order_number} synchronisée avec succès")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Aucun paiement associé à la commande {order.order_number}")
                )
                
        except Order.DoesNotExist:
            raise CommandError(f"Commande avec l'ID {order_id} non trouvée")

    def generate_report(self, dry_run, fix):
        """Génère un rapport des incohérences"""
        self.stdout.write("🔍 Analyse des incohérences entre commandes et paiements...")
        
        inconsistencies = get_status_consistency_report()
        
        if not inconsistencies:
            self.stdout.write(
                self.style.SUCCESS("✅ Aucune incohérence trouvée! Tous les statuts sont synchronisés.")
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f"⚠️ {len(inconsistencies)} incohérence(s) trouvée(s):")
        )
        
        for inconsistency in inconsistencies:
            self.stdout.write(f"""
📋 Commande {inconsistency['order_number']} (ID: {inconsistency['order_id']})
   Statut Order: {inconsistency['order_payment_status']}
   Statut Payment: {inconsistency['payment_status']}
   Statut attendu: {inconsistency['expected_payment_status']}
            """)
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING("Mode dry-run: aucune correction effectuée")
            )
            return
        
        if fix:
            self.stdout.write("🔧 Correction des incohérences...")
            fixed_count = 0
            
            with transaction.atomic():
                for inconsistency in inconsistencies:
                    try:
                        order = Order.objects.get(id=inconsistency['order_id'])
                        success = sync_order_payment_status(order, order.payment_status)
                        
                        if success:
                            fixed_count += 1
                            self.stdout.write(
                                f"✅ Commande {order.order_number} corrigée"
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"⚠️ Impossible de corriger la commande {order.order_number}")
                            )
                            
                    except Order.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"❌ Commande {inconsistency['order_id']} non trouvée")
                        )
            
            self.stdout.write(
                self.style.SUCCESS(f"🎉 {fixed_count}/{len(inconsistencies)} incohérence(s) corrigée(s)")
            )
        else:
            self.stdout.write(
                self.style.WARNING("Utilisez --fix pour corriger automatiquement les incohérences")
            )
