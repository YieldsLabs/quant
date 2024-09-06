use crate::types::{Period, Price, Rule, Scalar};
use crate::{ONE, ZERO};

#[derive(Debug, Clone, PartialEq)]
pub struct Series<T> {
    data: Vec<Option<T>>,
}

impl<T> IntoIterator for Series<T> {
    type Item = Option<T>;
    type IntoIter = std::vec::IntoIter<Self::Item>;

    fn into_iter(self) -> Self::IntoIter {
        self.data.into_iter()
    }
}

impl<T> FromIterator<Option<T>> for Series<T> {
    fn from_iter<I: IntoIterator<Item = Option<T>>>(iter: I) -> Self {
        Series {
            data: iter.into_iter().collect(),
        }
    }
}

impl<T> Series<T> {
    pub fn iter(&self) -> impl Iterator<Item = &Option<T>> {
        self.data.iter()
    }

    pub fn window(&self, period: Period) -> impl Iterator<Item = &[Option<T>]> + '_ {
        (0..self.len()).map(move |i| &self.data[i.saturating_sub(period - 1)..=i])
    }

    pub fn fmap<U, F>(&self, mut f: F) -> Series<U>
    where
        F: FnMut(Option<&T>) -> Option<U>,
    {
        self.iter().map(|x| f(x.as_ref())).collect()
    }

    pub fn zip_with<U, V, F>(&self, other: &Series<U>, mut f: F) -> Series<V>
    where
        F: FnMut(Option<&T>, Option<&U>) -> Option<V>,
        U: Clone,
    {
        self.iter()
            .zip(other.iter())
            .map(|(x, y)| f(x.as_ref(), y.as_ref()))
            .collect()
    }

    #[inline(always)]
    pub fn len(&self) -> usize {
        self.data.len()
    }
}

impl<T: Clone> Series<T> {
    pub fn shift(&self, period: Period) -> Self {
        let shifted_len = self.len().saturating_sub(period);

        core::iter::repeat(None)
            .take(period)
            .chain(self.iter().take(shifted_len).cloned())
            .collect()
    }

    pub fn empty(length: usize) -> Self {
        core::iter::repeat(None).take(length).collect()
    }

    pub fn last(&self) -> Option<T> {
        self.iter().last().cloned().flatten()
    }

    pub fn get(&self, index: usize) -> Option<T> {
        if index < self.len() {
            self.data[index].clone()
        } else {
            None
        }
    }
}

impl Price {
    pub fn nz(&self, replacement: Option<Scalar>) -> Self {
        self.fmap(|opt| match opt {
            Some(v) => Some(*v),
            None => Some(replacement.unwrap_or(ZERO)),
        })
    }

    pub fn na(&self) -> Rule {
        self.fmap(|val| Some(val.is_none()))
    }

    pub fn fill(scalar: Scalar, n: usize) -> Price {
        core::iter::repeat(scalar).take(n).collect()
    }

    pub fn zero(n: usize) -> Price {
        Series::fill(ZERO, n)
    }

    pub fn one(n: usize) -> Price {
        Series::fill(ONE, n)
    }
}

#[cfg(test)]
mod tests {
    use crate::series::Series;

    #[test]
    fn test_len() {
        let source = Series::from([4.0, 3.0, 2.0, 1.0]);
        let expected = 4;

        let result = source.len();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_from() {
        let source = Series::from([f32::NAN, 1.0, 2.0, 3.0]);
        let expected = Series::from([f32::NAN, 1.0, 2.0, 3.0]);

        assert_eq!(source, expected);
    }

    #[test]
    fn test_empty() {
        let len = 4;
        let expected = Series::from([f32::NAN, f32::NAN, f32::NAN, f32::NAN]);

        let result = Series::empty(len);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_nz() {
        let source = Series::from([f32::NAN, f32::NAN, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 0.0, 3.0, 4.0, 5.0]);

        let result = source.nz(Some(0.0));

        assert_eq!(result, expected);
    }

    #[test]
    fn test_shift() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, f32::NAN, 1.0, 2.0, 3.0]);
        let n = 2;

        let result = source.shift(n);

        assert_eq!(source.len(), result.len());
        assert_eq!(result, expected);
    }

    #[test]
    fn test_last() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Some(5.0);

        let result = source.last();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_last_none() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, f32::NAN]);
        let expected = None;

        let result = source.last();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_get() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Some(5.0);

        let result = source.get(4);

        assert_eq!(result, expected);
    }
}
