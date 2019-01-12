import datetime


class Asset(object):
    def __init__(self, *args, **kwargs):
        """
        Create an asset object
        :param args:
        :param kwargs: initial_price: the initial price of the asset, name: name of the asset
        """
        init_price = kwargs.get('initial_price', None)
        name = kwargs.get("name", None)
        if isinstance(init_price, (int, float)) and isinstance(name, (str)):
            self.__initial_price = init_price
            self.__actual_price = init_price
            # We're gonna store the price history
            self.__price_history = {datetime.datetime.now(): self.__actual_price}
            self.__name = name
        else:
            raise ValueError("The initial price should be a integer or a floating point number")

    @property
    def initial_price(self):
        return self.__initial_price

    @property
    def actual_price(self):
        return self.__actual_price

    @actual_price.setter
    def actual_price(self, val):
        self.__actual_price = val
        self.__price_history[datetime.datetime.now()] = self.__actual_price

    @property
    def price_history(self):
        return self.__price_history

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return "Asset: \n\t\t" \
               "Name: {name}\n\t\t" \
               "Initial price: {init_price}\n\t\t" \
               "Actual price: {act_price}\n\t\t" \
               "Price history: {price_hist}".format(name=self.name,
                                                    init_price=self.initial_price,
                                                    act_price=self.actual_price,
                                                    price_hist=self.price_history)


class Option(object):
    def __init__(self, *args, **kwargs):
        """
        An option is defined by its strike price and an asset
        :param args:
        :param kwargs: strike: The strike price of the option; asset: the asset concerned by the option, days: the options maturity
        """
        strike = kwargs.get('strike', None)
        asset = kwargs.get('asset', None)
        days = kwargs.get('days', None)
        if isinstance(strike, (int, float)) and isinstance(asset, Asset) and isinstance(days, int):
            self.__strike = strike
            self.__asset = asset
            self.__days = days
            self.__maturity = datetime.datetime.now() + datetime.timedelta(days=days)
        else:
            raise ValueError("The value of either the strike or the asset are of the wrong type")

    @property
    def strike(self):
        return self.__strike

    @property
    def days(self):
        return self.__days

    @property
    def asset(self):
        return self.__asset

    @property
    def maturity(self):
        return self.__maturity

    def __str__(self):
        return "Option: \n\t" \
               "{myasset} \n\t" \
               "Strike: {mystrike} \n\t" \
               "Maturity: {mymatu} \n\t".format(myasset=self.asset, mystrike=self.strike, mymatu=self.maturity)


class CallOption(Option):
    def __init__(self, *args, **kwargs):
        """
        A call option doesn't have extra parameters, however defining it separately allows us to define the
        payoff function which we are going to reuse for barrier options
        :param args:
        :param kwargs: strike: The strike price of the option; asset: the asset concerned by the option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return max(0, self.asset.actual_price - self.strike)

    def __str__(self):
        return super().__str__() + "Type: Call Option\n\t" \
                                   "Payoff: {payoff}\n\t".format(payoff=self.payoff())


class PutOption(Option):
    def __init__(self, *args, **kwargs):
        """
        We define a put option the same way we defined a call option
        :param args:
        :param kwargs: strike: The strike price of the option; asset: the asset concerned by the option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return max(0, self.strike - self.asset.actual_price)

    def __str__(self):
        return super().__str__() + "Type: Put Option\n\t" \
                                   "Payoff: {payoff}\n\t".format(payoff=self.payoff())


class BarrierOption(Option):
    def __init__(self, *args, **kwargs):
        """
        Creating a barrier option, which is defined as an option with a barrier price
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        barrier = kwargs.get('barrier', None)
        if isinstance(barrier, (int, float)):
            self.__barrier = barrier
        else:
            raise ValueError("The barrier price should be an integer or a floating point number")
        super().__init__(*args, **kwargs)

    @property
    def barrier(self):
        return self.__barrier

    def Mt(self):
        """
        :return: The Mt value of this option
        """
        return max(self.asset.price_history.values())

    def mt(self):
        """
        :return: The mt value of this option
        """
        return min(self.asset.price_history.values())

    def __str__(self):
        return super().__str__() + "Type: Barrier Option\n\t" \
                                   "Barrier: {barr}\n\t" \
                                   "Mt: {Mt}\n\t" \
                                   "mt: {mt}\n\t" \
                                   "Payoff: {payoff}\n\t".format(payoff=self.payoff(), barr=self.barrier,
                                                                 Mt=self.Mt(), mt=self.mt())


class UpAndInCall(CallOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Up and In Call Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.Mt() >= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Up and In Call"


class UpAndOutCall(CallOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Up and Out Call Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.Mt() <= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Up and Out Call"


class DownAndInCall(CallOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Down and In Call Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.mt() <= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Down and In Call"


class DownAndOutCall(CallOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Down and Out Call Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.mt() >= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Down and Out Call"


class UpAndInPut(PutOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Up and In Put Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.Mt() >= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Up and In Put"


class UpAndOutPut(PutOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Up and Out Put Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.Mt() <= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Up and Out Put"


class DownAndInPut(PutOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Down and In Put Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.mt() <= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Down and In Put"


class DownAndOutPut(PutOption, BarrierOption):
    def __init__(self, *args, **kwargs):
        """
        Modelization of a Down and Out Put Barrier Option, the arguments are the same that for a barrier option
        :param args:
        :param kwargs: barrier: the barrier price of this option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return super().payoff() if self.mt() >= self.barrier else 0

    def __str__(self):
        return BarrierOption.__str__(self) + "Barrier Type: Down and Out Put"


class LoopbackCall(CallOption):
    def __init__(self, *args, **kwargs):
        """
        Loopback call option, no extra parameter but the payoff function changes
        :param args:
        :param kwargs: strike: The strike price of the option; asset: the asset concerned by the option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return max(0, max(self.asset.price_history.values()) - self.strike)

    def __str__(self):
        return super().__str__() + "Type of Call: Loopback"


class LoopbackPut(PutOption):
    def __init__(self, *args, **kwargs):
        """
        Loopback put option, no extra parameter but the payoff function changes
        :param args:
        :param kwargs: strike: The strike price of the option; asset: the asset concerned by the option
        """
        super().__init__(*args, **kwargs)

    def payoff(self):
        return max(0, self.strike - min(self.asset.price_history.values()))

    def __str__(self):
        return super().__str__() + "Type of Put: Loopback"
