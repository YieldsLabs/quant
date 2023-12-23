use std::ops::{Index, IndexMut};

#[derive(Debug, Clone)]
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
    pub fn iter(&self) -> std::slice::Iter<'_, Option<T>> {
        self.data.iter()
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

    pub fn sliding_map<U, F>(&self, period: usize, mut f: F) -> Series<U>
    where
        F: FnMut(&[Option<T>], f32, usize) -> Option<U>,
        U: Clone,
    {
        let len = self.len();
        let mut data = vec![None; len];
        let mut window = vec![None; period];
        let mut pos = 0;

        for i in 0..len {
            window[pos] = self.data[i].clone();

            let size = (i + 1).min(period);

            data[i] = f(&window[0..size], size as f32, i);

            pos = (pos + 1) % period;
        }

        Series { data }
    }

    pub fn empty(length: usize) -> Self {
        std::iter::repeat(None).take(length).collect()
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn shift(&self, n: usize) -> Self {
        std::iter::repeat(None)
            .take(n)
            .chain(self.iter().take(self.len() - n).cloned())
            .collect()
    }

    pub fn last(&self) -> Option<T> {
        self.iter().last().cloned().flatten()
    }
}

impl<T: AsRef<[f32]>> From<T> for Series<f32> {
    fn from(item: T) -> Self {
        Self {
            data: item
                .as_ref()
                .iter()
                .map(|&x| if x.is_nan() { None } else { Some(x) })
                .collect(),
        }
    }
}

impl Series<f32> {
    fn extreme_value<F>(&self, period: usize, comparison: F) -> Self
    where
        F: Fn(&f32, &f32) -> bool,
    {
        self.sliding_map(period, |window, _, _| {
            window.iter().flatten().fold(None, |acc, &x| match acc {
                Some(acc_val) if comparison(&x, &acc_val) => Some(x),
                Some(_) => acc,
                None => Some(x),
            })
        })
    }

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
        Series::fill(0.0, len)
    }

    pub fn one(len: usize) -> Series<f32> {
        Series::fill(1.0, len)
    }

    pub fn change(&self, length: usize) -> Self {
        self - self.shift(length)
    }

    pub fn highest(&self, period: usize) -> Self {
        self.extreme_value(period, |a, b| a >= b)
    }

    pub fn lowest(&self, period: usize) -> Self {
        self.extreme_value(period, |a, b| a <= b)
    }
}

impl<T: PartialEq> PartialEq for Series<T> {
    fn eq(&self, other: &Self) -> bool {
        self.data == other.data
    }
}

impl PartialEq<Vec<Option<f32>>> for Series<f32> {
    fn eq(&self, other: &Vec<Option<f32>>) -> bool {
        &self.data == other
    }
}

impl From<Series<f32>> for Vec<f32> {
    fn from(val: Series<f32>) -> Self {
        val.into_iter().map(|x| x.unwrap_or(0.0)).collect()
    }
}

impl From<Series<bool>> for Vec<bool> {
    fn from(val: Series<bool>) -> Self {
        val.into_iter().map(|x| x.unwrap_or(false)).collect()
    }
}

impl From<Series<f32>> for Series<bool> {
    fn from(val: Series<f32>) -> Self {
        val.fmap(|opt| opt.map(|f| f.is_finite() && *f != 0.0))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_len() {
        let source = vec![4.0, 3.0, 2.0, 1.0];
        let expected = 4;

        let result = Series::from(&source);

        assert_eq!(result.len(), expected);
    }

    #[test]
    fn test_from() {
        let source = vec![f32::NAN, 1.0, 2.0, 3.0];
        let expected = vec![None, Some(1.0), Some(2.0), Some(3.0)];

        let result = Series::from(&source);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_empty() {
        let len = 4;
        let expected = vec![None, None, None, None];

        let result = Series::empty(len);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_shift() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let n = 2;
        let expected = vec![None, None, Some(1.0), Some(2.0), Some(3.0)];

        let result = Series::from(&source).shift(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_last() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = Some(5.0);

        let result = Series::from(&source).last();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_last_none() {
        let source = vec![1.0, 2.0, 3.0, 4.0, f32::NAN];
        let expected = None;

        let result = Series::from(&source).last();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_change() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = [
            None,
            Some(-0.25),
            Some(0.0599),
            Some(-0.540),
            Some(0.7199),
            Some(0.5),
            Some(0.2700),
            Some(0.3200),
            Some(0.4200),
        ];
        let series = Series::from(&source);

        let result = series.change(length);

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
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 3;
        let expected = vec![Some(1.0), Some(2.0), Some(3.0), Some(4.0), Some(5.0)];
        let series = Series::from(&source);

        let result = series.highest(period);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_lowest() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 3;
        let expected = vec![Some(1.0), Some(1.0), Some(1.0), Some(2.0), Some(3.0)];
        let series = Series::from(&source);

        let result = series.lowest(period);

        assert_eq!(result, expected);
    }
}
