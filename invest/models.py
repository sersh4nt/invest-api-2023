from django.db import models
from django.utils import timezone


class Account(models.Model):
    token = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    name = models.CharField(max_length=1000, blank=True)

    def __str__(self) -> str:
        return f"Account [{self.name}]"

    class Meta:
        db_table = "accounts"


class Subaccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    broker_id = models.BigIntegerField()
    type = models.IntegerChoices()
    name = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Subaccount [{self.name}] of account [{self.account.name}]"

    class Meta:
        db_table = "subaccounts"


class Currency(models.Model):
    iso = models.CharField(max_length=3, primary_key=True)
    figi = models.CharField(max_length=100)
    class_code = models.CharField(max_length=100)
    lot = models.IntegerField()
    name = models.CharField(max_length=1000)
    exchange = models.CharField(max_length=100)
    uid = models.CharField(max_length=100)
    api_trade_available = models.BooleanField(default=False)

    class Meta:
        db_table = "currencies"


class Instrument(models.Model):
    figi = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    class_code = models.CharField(max_length=100)
    lot = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=1000)
    exchange = models.CharField(max_length=100)
    uid = models.CharField(max_length=100)
    position_uid = models.CharField(max_length=100, null=True, default=None)
    api_trade_available = models.BooleanField(default=False)
    min_price_increment = models.DecimalField(max_digits=19, decimal_places=9)
    short_enabled_flag = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} [{self.ticker}]"

    class Meta:
        db_table = "instruments"


class Share(Instrument):
    ipo_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "shares"


class Bond(Instrument):
    coupon_quantity_per_year = models.IntegerField()
    maturiry_date = models.DateTimeField()
    nominal = models.DecimalField(max_digits=19, decimal_places=9)
    initial_nominal = models.DecimalField(max_digits=19, decimal_places=9)
    issue_size = models.IntegerField()
    floating_coupon_flag = models.BooleanField(default=True)

    class Meta:
        db_table = "bonds"


class ETF(Instrument):
    fixed_commission = models.DecimalField(max_digits=19, decimal_places=9)
    focus_type = models.CharField(max_length=100, blank=True)
    num_shares = models.DecimalField(max_digits=19, decimal_places=9)
    rebalancing_freq = models.CharField(max_length=100)

    class Meta:
        db_table = "etfs"


class Future(Instrument):
    first_trade_date = models.DateTimeField()
    last_trade_date = models.DateTimeField()
    futures_type = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=100)
    basic_asset = models.ForeignKey(Instrument, on_delete=models.SET_NULL, null=True)
    basic_asset_size = models.DecimalField(max_digits=19, decimal_places=9)
    expiration_date = models.DateTimeField()

    class Meta:
        db_table = "futures"


class Option(Instrument):
    direction = models.CharField(max_length=4, blank=True)
    payment_type = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    settlemet_type = models.CharField(max_length=100, blank=True)
    settlemet_currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True
    )
    asset_type = models.CharField(max_length=100)
    basic_asset = models.ForeignKey(Instrument, on_delete=models.SET_NULL, null=True)
    basic_asset_size = models.DecimalField(max_digits=19, decimal_places=9)
    strike_price = models.DecimalField(max_digits=19, decimal_places=9)

    class Meta:
        db_table = "options"


class PortfolioRecord(models.Model):
    subaccount = models.ForeignKey(Subaccount, on_delete=models.SET_NULL, null=True)
    ts = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "portfolio_records"


class PortfolioCost(models.Model):
    portfolio = models.ForeignKey(PortfolioRecord, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "portfolio_cost"


class PortfolioPosition(models.Model):
    portfolio = models.ForeignKey(PortfolioRecord, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL, null=True)
    blocked = models.DecimalField(max_digits=19, decimal_places=9)
    quantity = models.DecimalField(max_digits=19, decimal_places=9)
    average_price = models.DecimalField(max_digits=19, decimal_places=9)
    current_price = models.DecimalField(max_digits=19, decimal_places=9)
    var_margin = models.DecimalField(max_digits=19, decimal_places=9)
    expected_yield = models.DecimalField(max_digits=19, decimal_places=9)

    class Meta:
        db_table = "portfolio_positions"


class InstrumentIndex(models.Model):
    instrument = models.OneToOneField(
        Instrument, on_delete=models.SET_NULL, primary_key=True, null=True
    )
    is_enabled = models.BooleanField(default=True)
    volatility = models.FloatField()
    volume = models.FloatField()
    spread = models.FloatField()
    price = models.FloatField()
    gain = models.FloatField()
    relative_price = models.FloatField()

    class Meta:
        db_table = "instrument_index"


class Candle(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    ts = models.DateTimeField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.IntegerField()
    interval = models.CharField()

    class Meta:
        db_table = "candles"
