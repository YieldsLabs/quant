use std::ops::{Index, IndexMut};

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

impl<T> Index<usize> for Series<T> {
    type Output = Option<T>;

    fn index(&self, idx: usize) -> &Self::Output {
        &self.data[idx]
    }
}

impl<T> IndexMut<usize> for Series<T> {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.data[index]
    }
}

impl<T: Clone> Series<T> {
    pub fn iter(&self) -> impl Iterator<Item = &Option<T>> {
        self.data.iter()
    }

    pub fn window(&self, period: usize) -> impl Iterator<Item = &[Option<T>]> + '_ {
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

    pub fn empty(length: usize) -> Self {
        std::iter::repeat(None).take(length).collect()
    }

    #[inline]
    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn shift(&self, n: usize) -> Self {
        let shifted_len = self.len() - n;

        std::iter::repeat(None)
            .take(n)
            .chain(self.iter().take(shifted_len).cloned())
            .collect()
    }

    pub fn last(&self) -> Option<T> {
        self.iter().last().cloned().flatten()
    }
}

impl Series<f32> {
    pub fn nz(&self, replacement: Option<f32>) -> Self {
        self.fmap(|opt| match opt {
            Some(v) => Some(*v),
            None => Some(replacement.unwrap_or(0.0)),
        })
    }

    pub fn na(&self) -> Series<bool> {
        self.fmap(|val| Some(val.is_none()))
    }

    pub fn fill(scalar: f32, len: usize) -> Series<f32> {
        Series::empty(len).nz(Some(scalar))
    }

    pub fn zero(len: usize) -> Series<f32> {
        Series::fill(0., len)
    }

    pub fn one(len: usize) -> Series<f32> {
        Series::fill(1., len)
    }

    pub fn change(&self, length: usize) -> Self {
        self - self.shift(length)
    }

    pub fn highest(&self, period: usize) -> Self {
        self.window(period)
            .map(|w| {
                w.iter()
                    .flatten()
                    .max_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            })
            .collect()
    }

    pub fn lowest(&self, period: usize) -> Self {
        self.window(period)
            .map(|w| {
                w.iter()
                    .flatten()
                    .min_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
    fn test_shift() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, f32::NAN, 1.0, 2.0, 3.0]);
        let n = 2;

        let result = source.shift(n);

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
    fn test_change() {
        let source = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let length = 1;
        let epsilon = 0.001;
        let expected = Series::from([
            f32::NAN,
            -0.25,
            0.0599,
            -0.540,
            0.7199,
            0.5,
            0.2700,
            0.3200,
            0.4200,
        ]);

        let result = source.change(length);

        for i in 0..result.len() {
            match (result[i], expected[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!("at position {}: {:?} != {:?}", i, result[i], expected[i]),
            }
        }
    }

    #[test]
    fn test_highest() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let result = source.highest(period);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_lowest() {
        let source = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let expected = Series::from([f32::NAN, 2.0, 2.0, 1.0, 1.0]);
        let period = 3;

        let result = source.lowest(period);

        assert_eq!(result, expected);
    }
}
