use crate::{highest::highest, lowest::lowest};

pub fn stoch(high: &[f64], low: &[f64], close: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = high.len();

    if len != low.len() || len != close.len() || len < period {
        return vec![None; len];
    }

    let hh = highest(high, period);
    let ll = lowest(low, period);

    let mut stoch_values = vec![None; len];

    for i in (period - 1)..len {
        if let (Some(hh), Some(ll)) = (hh[i], ll[i]) {
            let stoch = 100.0 * (close[i] - ll) / (hh - ll);
            stoch_values[i] = Some(stoch);
        }
    }

    stoch_values
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stoch() {
        let high = vec![3.0, 3.0, 3.0, 3.0, 3.0];
        let low = vec![1.0, 1.0, 1.0, 1.0, 1.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];

        let expected = vec![None, None, Some(50.0), Some(25.0), Some(50.0)];

        let result = stoch(&high, &low, &close, 3);

        assert_eq!(result, expected);
    }
}
