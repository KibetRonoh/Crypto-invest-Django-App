from django.db import models
from datetime import datetime


class DailyLottery(models.Model):
    title = models.CharField(max_length=200)
    amount = models.IntegerField()
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class WeeklyLottery(models.Model):
    title = models.CharField(max_length=200)
    amount = models.IntegerField()
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

class SmartCoin(models.Model):
    title = models.CharField(max_length=200)
    value = models.IntegerField()
    sco_btc = models.DecimalField(max_digits=2, decimal_places=1)
    sco_eth = models.DecimalField(max_digits=2, decimal_places=1)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class HourlyFreeToken(models.Model):
    title = models.CharField(max_length=200)
    value = models.IntegerField()
    amount = models.IntegerField

    def __str__(self):
        return self.title



from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Proposed Bet holds all user's prop bets, which may or may not get accepted.

class ProposedBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    prop_text = models.CharField(max_length=256)
    prop_wager = models.IntegerField()
    max_wagers = models.IntegerField()
    remaining_wagers = models.IntegerField()
    end_date = models.DateTimeField()

    # win / loss / tie choices
    WIN = 1
    LOSS = -1
    TIE = 0
    WIN_LOSS_TIE_CHOICES = ((WIN, 'Win'), (LOSS, 'Loss'), (TIE, 'Tie'))

    won_bet = models.IntegerField(
        choices=WIN_LOSS_TIE_CHOICES,
        null=True,
        blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['end_date']
        verbose_name = 'Proposed Bet'

    verbose_name_plural = 'Proposed Bets'


# Accepted bet holds all prop bets that are accepted by another user
class AcceptedBet(models.Model):
    accepted_prop = models.ForeignKey(ProposedBet, on_delete=models.DO_NOTHING)
    accepted_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['accepted_prop__end_date']
        verbose_name = 'Accepted Bet'

    verbose_name_plural = 'Accpeted Bets'


# User Profile table holds some user info specific to this betting app

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(
        default=1000,
        help_text='The user\'s current balance. Every time the user settles up, the current balance is reset to zero.')
    overall_winnings = models.IntegerField(
        default=0, help_text='The user\'s overall winnings since joining.')
    get_prop_bet_emails = models.BooleanField(default=True)
    get_accepted_bet_emails = models.BooleanField(default=True)
    last_payment = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    verbose_name_plural = 'User Profiles'


# hook user profile to user table, so that it's created when a user is created
#

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


#
# end user profile hooks

# User Profile Audit creates an audit trail each time a user's winnings
# are updated due to an accepted bet being closed.

class UserProfileAudit(models.Model):
    user = models.ForeignKey(User, related_name='user_profile_user', on_delete=models.DO_NOTHING)
    admin_user = models.ForeignKey(User, related_name='user_profile_admin', on_delete=models.DO_NOTHING)
    accepted_bet = models.ForeignKey(AcceptedBet, on_delete=models.DO_NOTHING)
    original_current_balance = models.IntegerField()
    new_current_balance = models.IntegerField()
    original_overall_winnings = models.IntegerField()
    new_overall_winnings = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile Audit'

    verbose_name_plural = 'User Profile Audits'


class Deposit(models.Model):
    amount = models.IntegerField()
    method = models.CharField(max_length=100, blank=True)
    punter = models.CharField(max_length=100, blank=True)
    deposited_on = models.DateTimeField(auto_now_add=True)
    deposit_id = models.CharField(max_length=100, blank=True)
    success = models.BooleanField(default=False)


class Withdraw(models.Model):
    amount = models.IntegerField()
    paypal = models.CharField(max_length=100, blank=True)
    paypal2 = models.CharField(max_length=100, blank=True)
    skrill = models.CharField(max_length=100, blank=True)
    skrill2 = models.CharField(max_length=100, blank=True)
    bank_transfer = models.TextField(max_length=1000, blank=True)
