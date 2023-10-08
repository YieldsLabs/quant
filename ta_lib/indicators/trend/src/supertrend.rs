use core::{iff, Series};

pub fn supertrend(
    hl2: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> Series<f32> {
    let atr_mul = atr * factor;
    let basic_upper_band = hl2 + &atr_mul;
    let basic_lower_band = hl2 - &atr_mul;

    let prev_upper_band = basic_upper_band.shift(1);
    let prev_lower_band = basic_lower_band.shift(1);

    let prev_final_upper_band = iff!(prev_upper_band.na(), basic_upper_band, prev_upper_band);
    let prev_final_lower_band = iff!(prev_lower_band.na(), basic_lower_band, prev_lower_band);
    let prev_close = close.shift(1);

    let cond_upper =
        basic_upper_band.lt(&prev_final_upper_band) | prev_close.gt(&prev_final_upper_band);
    let cond_lower =
        basic_lower_band.gt(&prev_final_lower_band) | prev_close.lt(&prev_final_lower_band);

    let final_upper_band = iff!(cond_upper, &basic_upper_band, &prev_final_upper_band);
    let final_lower_band = iff!(cond_lower, &basic_lower_band, &prev_final_lower_band);

    let cond1 = final_lower_band.eq(&prev_final_lower_band) & close.lt(&final_lower_band);
    let cond2 = final_lower_band.eq(&prev_final_lower_band) & close.gte(&final_lower_band);
    let cond3 = final_lower_band.eq(&prev_final_upper_band) & close.gt(&final_upper_band);
    let cond4 = final_lower_band.eq(&prev_final_upper_band) & close.lte(&final_upper_band);

    iff!(
        cond4,
        final_upper_band,
        iff!(
            cond3,
            final_lower_band,
            iff!(
                cond2,
                final_lower_band,
                iff!(cond1, final_upper_band, final_upper_band)
            )
        )
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::median_price;
    use volatility::atr;

    #[test]
    fn test_supertrend() {
        let high = Series::from([
            7.1135, 7.1135, 7.116, 7.1225, 7.121, 7.136, 7.142, 7.1405, 7.1125, 7.1360, 7.1350,
            7.1550, 7.1590, 7.1505, 7.1460, 7.1505, 7.1555, 7.1575, 7.1550, 7.1445, 7.1540, 7.1525,
            7.1495, 7.1390, 7.1375, 7.1395, 7.1290, 7.1280, 7.1280, 7.1355, 7.1280, 7.1310, 7.1275,
            7.1250, 7.1270, 7.1230, 7.1210, 7.1325, 7.1355, 7.142, 7.14, 7.1260, 7.1870,
        ]);
        let low = Series::from([
            7.0935, 7.088, 7.088, 7.1075, 7.1135, 7.1185, 7.119, 7.112, 7.1, 7.1055, 7.1160,
            7.1285, 7.1480, 7.1375, 7.1370, 7.1405, 7.1440, 7.1460, 7.1375, 7.1355, 7.1440, 7.1420,
            7.1365, 7.1280, 7.1305, 7.1250, 7.1145, 7.1035, 7.1135, 7.1175, 7.1220, 7.1225, 7.1180,
            7.1180, 7.1125, 7.1055, 7.1115, 7.12, 7.126, 7.1295, 7.114, 7.1160, 7.1235,
        ]);
        let close = Series::from([
            7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112, 7.1095, 7.1220, 7.1310,
            7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415, 7.1445, 7.1525, 7.1440,
            7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220, 7.1230, 7.1225, 7.1180,
            7.1250, 7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235, 7.1645,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 2;
        let atr = atr(&high, &low, &close, atr_period, Some("SMMA"));

        let factor = 3.0;
        let expected = vec![
            7.0435004, 7.0435004, 7.0324993, 7.1755624, 7.158781, 7.158781, 7.080235, 7.0724916,
            7.0544963, 7.0516224, 7.190532, 7.190532, 7.206133, 7.1008663, 7.177908, 7.177908,
            7.178704, 7.1836014, 7.1175737, 7.175169, 7.175169, 7.116416, 7.115208, 7.1074786,
            7.16163, 7.1063695, 7.0966845, 7.082217, 7.170758, 7.170758, 7.1600013, 7.157001,
            7.096499, 7.1466875, 7.0963125, 7.085407, 7.1522107, 7.1522107, 7.162981, 7.1633654,
            7.100692, 7.1642647, 7.077736,
        ];

        let result: Vec<f32> = supertrend(&hl2, &close, &atr, factor).into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result, expected);
    }
}
