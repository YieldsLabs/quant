use crate::traits::{Comparator, Cross};
use crate::types::{Price, Rule, Scalar};

impl Cross<Scalar> for Price {
    type Output = Rule;

    fn cross_over(&self, line: &Scalar) -> Self::Output {
        self.sgt(line) & self.shift(1).slt(line)
    }

    fn cross_under(&self, line: &Scalar) -> Self::Output {
        self.slt(line) & self.shift(1).sgt(line)
    }

    fn cross(&self, line: &Scalar) -> Self::Output {
        self.cross_over(line) | self.cross_under(line)
    }
}

impl Cross<Price> for Price {
    type Output = Rule;

    fn cross_over(&self, rhs: &Price) -> Self::Output {
        self.sgt(rhs) & self.shift(1).slt(&rhs.shift(1))
    }

    fn cross_under(&self, rhs: &Price) -> Self::Output {
        self.slt(rhs) & self.shift(1).sgt(&rhs.shift(1))
    }

    fn cross(&self, rhs: &Price) -> Self::Output {
        self.cross_over(rhs) | self.cross_under(rhs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::series::Series;

    #[test]
    fn test_cross_over() {
        let a = Series::from([5.5, 5.0, 4.5, 3.0, 2.5]);
        let b = Series::from([4.5, 2.0, 3.0, 3.5, 2.0]);
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 0.0, 1.0]).into();

        let result = a.cross_over(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_cross_under() {
        let a = Series::from([5.5, 5.0, 4.5, 3.0, 2.5]);
        let b = Series::from([4.5, 2.0, 3.0, 3.5, 2.0]);
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.cross_under(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_cross() {
        let a = Series::from([5.5, 5.0, 4.5, 3.0, 2.5]);
        let b = Series::from([4.5, 2.0, 3.0, 3.5, 2.0]);
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 1.0, 1.0]).into();

        let result = a.cross(&b);

        assert_eq!(result, expected);
    }
}
