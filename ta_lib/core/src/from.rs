use crate::series::Series;

impl<T: AsRef<[f32]>> From<T> for Series<f32> {
    fn from(item: T) -> Self {
        item.as_ref()
            .iter()
            .map(|&x| if x.is_nan() { None } else { Some(x) })
            .collect()
    }
}

impl<'a> FromIterator<Option<&'a f32>> for Series<f32> {
    fn from_iter<I: IntoIterator<Item = Option<&'a f32>>>(iter: I) -> Self {
        iter.into_iter().map(|opt| opt.map(|&x| x)).collect()
    }
}

impl FromIterator<f32> for Series<f32> {
    fn from_iter<I: IntoIterator<Item = f32>>(iter: I) -> Self {
        iter.into_iter()
            .map(|x| if x.is_nan() { None } else { Some(x) })
            .collect()
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
        val.fmap(|opt| opt.map(|f| f.is_finite() && *f != 0.))
    }
}
