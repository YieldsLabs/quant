use crate::constants::ZERO;
use crate::series::Series;
use crate::traits::Operation;
use crate::types::{Price, Rule, Scalar};
use std::ops::{Add, Div, Mul, Sub};

impl Operation<Scalar, Scalar, Scalar> for Price {
    type Output = Price;

    fn ops<F>(&self, scalar: &Scalar, op: F) -> Self::Output
    where
        F: Fn(Scalar, Scalar) -> Scalar,
    {
        self.fmap(|val| val.map(|v| op(*v, *scalar)))
    }

    fn sadd(&self, scalar: &Scalar) -> Self::Output {
        self.ops(scalar, |v, s| v + s)
    }

    fn smul(&self, scalar: &Scalar) -> Self::Output {
        self.ops(scalar, |v, s| v * s)
    }

    fn sdiv(&self, scalar: &Scalar) -> Self::Output {
        self.ops(scalar, |v, s| if s != ZERO { v / s } else { ZERO })
    }

    fn ssub(&self, scalar: &Scalar) -> Self::Output {
        self.ops(scalar, |v, s| v - s)
    }
}

impl Operation<Price, Scalar, Scalar> for Price {
    type Output = Price;

    fn ops<F>(&self, rhs: &Price, op: F) -> Self::Output
    where
        F: Fn(Scalar, Scalar) -> Scalar,
    {
        self.zip_with(rhs, |a, b| {
            a.and_then(|a_val| b.map(|b_val| op(*a_val, *b_val)))
        })
    }

    fn sadd(&self, rhs: &Price) -> Self::Output {
        self.ops(rhs, |v, s| v + s)
    }

    fn smul(&self, rhs: &Price) -> Self::Output {
        self.ops(rhs, |v, s| v * s)
    }

    fn sdiv(&self, rhs: &Price) -> Self::Output {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(_a_val), Some(b_val)) if *b_val == ZERO => Some(ZERO),
            (Some(a_val), Some(b_val)) if *b_val != ZERO => Some(a_val / b_val),
            _ => None,
        })
    }

    fn ssub(&self, rhs: &Price) -> Self::Output {
        self.ops(rhs, |v, s| v - s)
    }
}

impl Operation<Price, bool, Scalar> for Rule {
    type Output = Price;

    fn ops<F>(&self, rhs: &Price, op: F) -> Self::Output
    where
        F: Fn(bool, Scalar) -> Scalar,
    {
        self.zip_with(rhs, |b, a| match (b, a) {
            (Some(b_val), Some(a_val)) => Some(op(*b_val, *a_val)),
            _ => None,
        })
    }

    fn sadd(&self, _rhs: &Price) -> Self::Output {
        unimplemented!()
    }

    fn smul(&self, rhs: &Price) -> Self::Output {
        self.ops(rhs, |b, a| if b { a } else { ZERO })
    }

    fn sdiv(&self, _rhs: &Price) -> Self::Output {
        unimplemented!()
    }

    fn ssub(&self, _rhs: &Price) -> Self::Output {
        unimplemented!()
    }
}

macro_rules! impl_series_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<Price> for &Price {
            type Output = Price;

            fn $trait_method(self, rhs: Price) -> Self::Output {
                self.$method(&rhs)
            }
        }

        impl $trait_name<&Price> for Price {
            type Output = Price;

            fn $trait_method(self, rhs: &Price) -> Self::Output {
                self.$method(rhs)
            }
        }

        impl $trait_name<&Price> for &Price {
            type Output = Price;

            fn $trait_method(self, rhs: &Price) -> Self::Output {
                self.$method(rhs)
            }
        }

        impl $trait_name<Price> for Price {
            type Output = Price;

            fn $trait_method(self, rhs: Price) -> Self::Output {
                self.$method(&rhs)
            }
        }
    };
}

impl_series_ops!(Add, add, sadd);
impl_series_ops!(Mul, mul, smul);
impl_series_ops!(Div, div, sdiv);
impl_series_ops!(Sub, sub, ssub);

macro_rules! impl_scalar_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<&Price> for Scalar {
            type Output = Price;

            fn $trait_method(self, rhs: &Price) -> Self::Output {
                rhs.$method(&self)
            }
        }

        impl $trait_name<Price> for Scalar {
            type Output = Price;

            fn $trait_method(self, rhs: Price) -> Self::Output {
                rhs.$method(&self)
            }
        }

        impl $trait_name<Scalar> for &Price {
            type Output = Price;

            fn $trait_method(self, scalar: Scalar) -> Self::Output {
                self.$method(&scalar)
            }
        }

        impl $trait_name<Scalar> for Price {
            type Output = Price;

            fn $trait_method(self, scalar: Scalar) -> Self::Output {
                self.$method(&scalar)
            }
        }
    };
}

impl_scalar_ops!(Add, add, sadd);
impl_scalar_ops!(Mul, mul, smul);

impl Div<Scalar> for &Price {
    type Output = Price;

    fn div(self, scalar: Scalar) -> Self::Output {
        self.sdiv(&scalar)
    }
}

impl Div<Scalar> for Price {
    type Output = Price;

    fn div(self, scalar: Scalar) -> Self::Output {
        self.sdiv(&scalar)
    }
}

impl Div<&Price> for Scalar {
    type Output = Price;

    fn div(self, rhs: &Price) -> Self::Output {
        Series::fill(self, rhs.len()).sdiv(rhs)
    }
}

impl Div<Price> for Scalar {
    type Output = Price;

    fn div(self, rhs: Price) -> Self::Output {
        Series::fill(self, rhs.len()).sdiv(&rhs)
    }
}

impl Sub<Scalar> for &Price {
    type Output = Price;

    fn sub(self, scalar: Scalar) -> Self::Output {
        self.ssub(&scalar)
    }
}

impl Sub<Scalar> for Price {
    type Output = Price;

    fn sub(self, scalar: Scalar) -> Self::Output {
        self.ssub(&scalar)
    }
}

impl Sub<&Price> for Scalar {
    type Output = Price;

    fn sub(self, rhs: &Price) -> Self::Output {
        rhs.negate().ssub(&-self)
    }
}

impl Sub<Price> for Scalar {
    type Output = Price;

    fn sub(self, rhs: Price) -> Self::Output {
        rhs.negate().ssub(&-self)
    }
}

macro_rules! impl_bool_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<&Price> for &Rule {
            type Output = Price;

            fn $trait_method(self, rhs: &Price) -> Self::Output {
                self.$method(rhs)
            }
        }

        impl $trait_name<&Price> for Rule {
            type Output = Price;

            fn $trait_method(self, rhs: &Price) -> Self::Output {
                self.$method(rhs)
            }
        }
    };
}

impl_bool_ops!(Mul, mul, smul);
