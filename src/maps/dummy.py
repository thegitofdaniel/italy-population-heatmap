from pydantic import BaseModel, Field


class InterestRate(BaseModel):
    value: float | int
    freq: str = Field(..., strip_whitespace=True, to_upper=True, pattern=r"^[YSQMD]$")
    regime: str = Field(
        ...,
        strip_whitespace=True,
        to_upper=False,
        pattern=r"^(simple|compound|continuous)$",
    )

    def __str__(self):
        return f"InterestRate(value={self.value:.4f}, freq='{self.freq}', regime='{self.regime}')"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        # equivalent rates are not the same!
        assert isinstance(other, InterestRate)

        if self.freq != other.freq:
            other = other.convert_to_equivalent(new_freq=self.freq)
        if self.regime != other.regime:
            return self.convert_to_compound().value == self.convert_to_compound().value
        else:
            return self.value == other.value

    def __gt__(self, other):
        assert isinstance(other, InterestRate)
        if self.freq != other.freq:
            other = other.convert_to_equivalent(new_freq=self.freq)
        if self.regime != other.regime:
            return self.convert_to_compound().value > self.convert_to_compound().value
        else:
            return self.value > other.value

    def __lt__(self, other):
        assert isinstance(other, InterestRate)
        if self.freq != other.freq:
            other = other.convert_to_equivalent(new_freq=self.freq)
        if self.regime != other.regime:
            return self.convert_to_compound().value < self.convert_to_compound().value
        else:
            return self.value < other.value
