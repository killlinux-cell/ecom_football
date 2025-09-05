"""
Commande Django pour recalculer les totaux de toutes les commandes
"""

from django.core.management.base import BaseCommand
from orders.models import Order


class Command(BaseCommand):
    help = 'Recalcule les totaux de toutes les commandes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les corrections qui seraient effectuées sans les appliquer',
        )
        parser.add_argument(
            '--order-number',
            type=str,
            help='Recalcule uniquement la commande avec ce numéro',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        order_number = options['order_number']
        
        if order_number:
            orders = Order.objects.filter(order_number=order_number)
            if not orders.exists():
                self.stdout.write(
                    self.style.ERROR(f"❌ Commande {order_number} non trouvée")
                )
                return
        else:
            orders = Order.objects.all()
        
        self.stdout.write(f"🔍 Analyse de {orders.count()} commande(s)...")
        
        incohérentes = 0
        corrigées = 0
        
        for order in orders:
            # Vérifier l'incohérence
            if not order.validate_totals():
                incohérentes += 1
                
                # Calculer les nouveaux totaux
                total_articles = sum(item.total_price for item in order.items.all())
                new_subtotal = total_articles
                new_total = total_articles + order.shipping_cost
                
                self.stdout.write(f"\n⚠️ Commande {order.order_number}:")
                self.stdout.write(f"   - Sous-total actuel: {order.subtotal} FCFA")
                self.stdout.write(f"   - Nouveau sous-total: {new_subtotal} FCFA")
                self.stdout.write(f"   - Total actuel: {order.total} FCFA")
                self.stdout.write(f"   - Nouveau total: {new_total} FCFA")
                self.stdout.write(f"   - Articles: {order.items.count()}")
                
                if not dry_run:
                    # Corriger la commande
                    order.recalculate_totals()
                    self.stdout.write(f"   ✅ Corrigée")
                    corrigées += 1
                else:
                    self.stdout.write(f"   🔍 [DRY-RUN] Serait corrigée")
        
        # Résumé
        self.stdout.write(f"\n📊 RÉSUMÉ:")
        self.stdout.write(f"   - Commandes analysées: {orders.count()}")
        self.stdout.write(f"   - Commandes incohérentes: {incohérentes}")
        
        if dry_run:
            self.stdout.write(f"   - Mode dry-run: Aucune correction appliquée")
            self.stdout.write(
                self.style.WARNING("Utilisez sans --dry-run pour appliquer les corrections")
            )
        else:
            self.stdout.write(f"   - Commandes corrigées: {corrigées}")
            if corrigées > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"🎉 {corrigées} commande(s) corrigée(s) avec succès!")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("✅ Toutes les commandes sont cohérentes!")
                )
