use std::iter::repeat;
use std::ops::{Index, IndexMut};

#[derive(Debug, Clone)]
pub struct Series<T> {
    data: Vec<Option<T>>,
}

impl<T: Clone> Series<T> {
    pub fn fmap<U, F>(&self, mut f: F) -> Series<U>
    where
        F: FnMut(Option<&T>) -> Option<U>,
    {
        Series {
            data: self.data.iter().map(|x| f(x.as_ref())).collect(),
        }
    }

    pub fn zip_with<U, V, F>(self, other: &Series<U>, mut f: F) -> Series<V>
    where
        F: FnMut(Option<T>, Option<U>) -> Option<V>,
        U: Clone,
    {
        let data = self
            .data
            .into_iter()
            .zip(other.data.clone().into_iter())
            .map(|(x, y)| f(x, y))
            .collect();

        Series { data }
    }

    pub fn empty(length: usize) -> Self {
        Self {
            data: repeat(None).take(length).collect(),
        }
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn shift(&self, n: usize) -> Self {
        let data = repeat(None)
            .take(n)
            .chain(self.data.iter().cloned().skip(n))
            .collect();

        Self { data }
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

impl Series<f64> {
    fn extreme_value<F>(&self, period: usize, comparison: F) -> Self
    where
        F: Fn(&f64, &f64) -> bool,
    {
        let len = self.len();
        let mut extreme_values = Self::empty(len);
        let mut indices: Vec<usize> = Vec::new();

        for i in 0..len {
            let start = if i >= period { i - period + 1 } else { 0 };

            indices.retain(|&j| j >= start);
            indices.retain(|&j| {
                comparison(&self[j].unwrap_or(f64::NAN), &self[i].unwrap_or(f64::NAN))
            });

            indices.push(i);

            extreme_values[i] = self[indices[0]].clone();
        }

        extreme_values
    }

    pub fn nz(&self, replacement: Option<f64>) -> Self {
        let replacement = replacement.unwrap_or(0.0);

        self.fmap(|opt| match opt {
            Some(v) => Some(*v),
            None => Some(replacement),
        })
    }

    pub fn change(&self, length: usize) -> Self {
        let len = self.len();
        let mut change = Self::empty(len);

        for i in length..len {
            if let (Some(current), Some(prev)) = (self[i], self[i - length]) {
                change[i] = Some(current - prev);
            }
        }

        change
    }

    pub fn highest(&self, period: usize) -> Self {
        self.extreme_value(period, |a, b| a >= b)
    }

    pub fn lowest(&self, period: usize) -> Self {
        self.extreme_value(period, |a, b| a <= b)
    }
}

impl<T: AsRef<[f64]>> From<T> for Series<f64> {
    fn from(item: T) -> Self {
        Self {
            data: item.as_ref().iter().map(|&x| Some(x)).collect(),
        }
    }
}

impl Into<Vec<f64>> for Series<f64> {
    fn into(self) -> Vec<f64> {
        self.data.into_iter().filter_map(|x| x).collect()
    }
}

impl PartialEq<Vec<Option<f64>>> for Series<f64> {
    fn eq(&self, other: &Vec<Option<f64>>) -> bool {
        &self.data == other
    }
}

impl Series<bool> {}

impl PartialEq<Vec<Option<bool>>> for Series<bool> {
    fn eq(&self, other: &Vec<Option<bool>>) -> bool {
        &self.data == other
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
    fn test_change() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = vec![
            None,
            Some(-0.25),
            Some(0.0599),
            Some(-0.539),
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
