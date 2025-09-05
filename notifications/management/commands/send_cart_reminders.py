"""
Commande Django pour envoyer les rappels de panier abandonné
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notifications.email_service import email_service
from django.contrib.auth.models import User
from cart.models import CartItem
from notifications.models import EmailLog


class Command(BaseCommand):
    help = 'Envoie les rappels de panier abandonné'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Nombre d\'heures après lesquelles envoyer le rappel (défaut: 24)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les rappels qui seraient envoyés sans les envoyer',
        )

    def handle(self, *args, **options):
        hours = options['hours']
        dry_run = options['dry_run']
        
        self.stdout.write(f"🔍 Recherche des paniers abandonnés depuis {hours}h...")
        
        # Récupérer les utilisateurs avec des paniers abandonnés
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        # Récupérer les utilisateurs uniques avec des paniers
        users_with_carts = User.objects.filter(
            cart__items__created_at__lt=cutoff_time
        ).distinct()
        
        if not users_with_carts.exists():
            self.stdout.write(
                self.style.SUCCESS("✅ Aucun panier abandonné trouvé!")
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f"⚠️ {users_with_carts.count()} utilisateur(s) avec panier abandonné trouvé(s)")
        )
        
        sent_count = 0
        skipped_count = 0
        
        for user in users_with_carts:
            # Récupérer les articles du panier
            cart_items = CartItem.objects.filter(
                cart__user=user,
                created_at__lt=cutoff_time
            )
            
            if not cart_items.exists():
                continue
            
            # Vérifier si un rappel n'a pas déjà été envoyé
            existing_reminder = EmailLog.objects.filter(
                user=user,
                template__template_type='cart_reminder',
                created_at__gte=cutoff_time
            ).exists()
            
            if existing_reminder:
                self.stdout.write(f"⏭️ Rappel déjà envoyé à {user.email}")
                skipped_count += 1
                continue
            
            if dry_run:
                self.stdout.write(f"📧 Rappel à envoyer à {user.email} ({cart_items.count()} articles)")
                continue
            
            # Envoyer le rappel
            try:
                success = email_service.send_cart_reminder(user, cart_items)
                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Rappel envoyé à {user.email}")
                    )
                    sent_count += 1
                else:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Erreur envoi à {user.email}")
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Erreur envoi à {user.email}: {str(e)}")
                )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f"Mode dry-run: {users_with_carts.count()} rappel(s) seraient envoyés")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"🎉 {sent_count} rappel(s) envoyé(s), {skipped_count} ignoré(s)")
            )
