use core::prelude::*;

pub fn md(source: &Price, period: Period) -> Price {
    let len = source.len();

    let mut mg = Series::empty(len);
    let seed = source.smooth(Smooth::EMA, period);

    for _ in 0..len {
        let prev_mg = nz!(mg.shift(1), seed);
        mg = &prev_mg + (source - &prev_mg) / ((source / &prev_mg).pow(4) * period as Scalar);
    }

    mg
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_md() {
        let source = Series::from([
            19.512, 19.511, 19.534, 19.527, 19.536, 19.565, 19.571, 19.606, 19.594, 19.575,
        ]);
        let expected = vec![
            19.512, 19.511665, 19.519077, 19.521713, 19.52646, 19.539206, 19.549734, 19.568275,
            19.576805, 19.576_204,
        ];

        let result: Vec<Scalar> = md(&source, 3).into();

        assert_eq!(result, expected);
    }
}
