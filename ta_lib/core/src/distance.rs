use crate::series::Series;

impl Series<f32> {
    pub fn ad(&self, period: usize) -> Self {
        self - self.ma(period)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_average_distance() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 0.5, 1.0, 1.0, 1.0]);
        let period = 3;

        let result = source.ad(period);

        assert_eq!(result, expected);
    }
}
