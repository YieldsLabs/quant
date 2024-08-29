use crate::constants::ZERO;
use crate::types::{Price, Rule, Scalar};

impl<T: AsRef<[Scalar]>> From<T> for Price {
    fn from(item: T) -> Self {
        item.as_ref()
            .iter()
            .map(|&x| if x.is_nan() { None } else { Some(x) })
            .collect()
    }
}

impl<'a> FromIterator<Option<&'a Scalar>> for Price {
    fn from_iter<I: IntoIterator<Item = Option<&'a Scalar>>>(iter: I) -> Self {
        iter.into_iter().map(|opt| opt.copied()).collect()
    }
}

impl FromIterator<Scalar> for Price {
    fn from_iter<I: IntoIterator<Item = Scalar>>(iter: I) -> Self {
        iter.into_iter()
            .map(|x| if x.is_nan() { None } else { Some(x) })
            .collect()
    }
}

impl From<Price> for Vec<Scalar> {
    fn from(val: Price) -> Self {
        val.into_iter().map(|x| x.unwrap_or(ZERO)).collect()
    }
}

impl From<Rule> for Vec<bool> {
    fn from(val: Rule) -> Self {
        val.into_iter().map(|x| x.unwrap_or(false)).collect()
    }
}

impl From<Price> for Rule {
    fn from(val: Price) -> Self {
        val.fmap(|opt| opt.map(|f| f.is_finite() && *f != ZERO))
    }
}
