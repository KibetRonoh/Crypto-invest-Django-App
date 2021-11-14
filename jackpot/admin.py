from django.contrib import admin
from .models import ProposedBet, AcceptedBet, UserProfile, UserProfileAudit, Withdraw, Deposit
from .models import WeeklyLottery, DailyLottery, SmartCoin, HourlyFreeToken


class WeeklyLotteryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    list_filter = ('amount',)
    search_fields = ('title',)
    list_per_page = 25


class ProposedBetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prop_text', 'prop_wager', 'max_wagers', 'remaining_wagers', 'end_date')
    list_display_links = ('id', 'user', 'prop_text')
    search_fields = ('id', 'user', 'prop_text', 'prop_wager', 'max_wagers', 'remaining_wagers', 'end_date')
    list_per_page = 25


class AcceptedBetAdmin(admin.ModelAdmin):
    list_display = ('id', 'accepted_prop', 'accepted_user', 'created_on', 'modified_on', 'is_complete')
    list_display_links = ('id', 'accepted_prop', 'accepted_user')
    search_fields = ('id', 'accepted_user', 'created_on', 'modified_on')
    list_per_page = 25


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'current_balance', 'overall_winnings', 'get_prop_bet_emails', 'get_accepted_bet_emails',
    'last_payment', 'created_on', 'modified_on')
    list_display_links = ('id', 'user', 'current_balance', 'overall_winnings', 'get_prop_bet_emails')
    search_fields = ('user', 'current_balance', 'overall_winnings', 'get_prop_bet_emails')
    list_per_page = 25


class UserProfileAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'admin_user', 'accepted_bet', 'original_current_balance', 'new_current_balance',
                    'original_overall_winnings', 'new_overall_winnings', 'created_on')
    list_display_links = ('id', 'user', 'admin_user')
    search_fields = ('id', 'user', 'admin_user', 'accepted_bet', 'original_current_balance', 'new_current_balance',
                     'original_overall_winnings')
    list_per_page = 25


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'paypal', 'paypal2', 'skrill', 'skrill2', 'bank_transfer')
    list_display_links = ('id', 'amount', 'paypal')
    search_fields = ('id', 'amount', 'paypal', 'paypal2', 'skrill', 'skrill2', 'bank_transfer')
    list_per_page = 25


class DepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'method', 'punter', 'success', 'deposit_id', 'deposited_on')
    list_display_links = ('id', 'amount', 'method', 'punter')
    list_per_page = 25


class HourlyFreeTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_per_page = 25


class SmartCoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_per_page = 25


class DailyLotteryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_per_page = 25


admin.site.register(WeeklyLottery, WeeklyLotteryAdmin)
admin.site.register(DailyLottery, DailyLotteryAdmin)
admin.site.register(SmartCoin, SmartCoinAdmin)
admin.site.register(HourlyFreeToken, HourlyFreeTokenAdmin)

admin.site.register(ProposedBet, ProposedBetAdmin)
admin.site.register(AcceptedBet, AcceptedBetAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfileAudit, UserProfileAuditAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
admin.site.register(Deposit, DepositAdmin)
