use core::prelude::*;

pub fn supertrend(
    hl2: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> (Series<f32>, Series<f32>) {
    let atr_mul = atr * factor;

    let mut up = hl2 - &atr_mul;
    let mut dn = hl2 + &atr_mul;

    let len = hl2.len();
    let prev_close = close.shift(1);

    for _ in 0..len {
        let mut prev_up = up.shift(1);
        let mut prev_dn = dn.shift(1);

        prev_up = iff!(prev_up.na(), up, prev_up);
        prev_dn = iff!(prev_dn.na(), dn, prev_dn);

        up = iff!(prev_close.sgt(&prev_up), up.max(&prev_up), up);
        dn = iff!(prev_close.slt(&prev_dn), dn.min(&prev_dn), dn);
    }

    let mut direction = Series::empty(len);
    let trend_up = Series::one(len);
    let trend_dn = -1.0 * &trend_up;

    let prev_up = up.shift(1);
    let prev_dn = dn.shift(1);

    for _ in 0..len {
        let prev_direction = direction.shift(1);

        direction = iff!(prev_direction.na(), trend_up, prev_direction);
        direction = iff!(close.slt(&prev_up), trend_dn, direction);
        direction = iff!(close.sgt(&prev_dn), trend_up, direction);
    }

    let supertrend = iff!(direction.seq(&1.0), up, dn);

    (direction, supertrend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;
    use volatility::atr;

    #[test]
    fn test_supertrend() {
        let high = Series::from([
            7.1135, 7.1135, 7.116, 7.1225, 7.121, 7.136, 7.142, 7.1405, 7.1125, 7.1360, 7.1350,
            7.1550, 7.1590, 7.1505, 7.1460, 7.1505, 7.1555, 7.1575, 7.1550, 7.1445, 7.1540, 7.1525,
            7.1495, 7.1390, 7.1375, 7.1395, 7.1290, 7.1280, 7.1280, 7.1355, 7.1280, 7.1310, 7.1275,
            7.1250, 7.1270, 7.1230, 7.1210, 7.1325, 7.1355, 7.142, 7.14, 7.1260, 7.1870, 7.1670,
            7.1580,
        ]);
        let low = Series::from([
            7.0935, 7.088, 7.088, 7.1075, 7.1135, 7.1185, 7.119, 7.112, 7.1, 7.1055, 7.1160,
            7.1285, 7.1480, 7.1375, 7.1370, 7.1405, 7.1440, 7.1460, 7.1375, 7.1355, 7.1440, 7.1420,
            7.1365, 7.1280, 7.1305, 7.1250, 7.1145, 7.1035, 7.1135, 7.1175, 7.1220, 7.1225, 7.1180,
            7.1180, 7.1125, 7.1055, 7.1115, 7.12, 7.126, 7.1295, 7.114, 7.1160, 7.1235, 7.1565,
            7.1510,
        ]);
        let close = Series::from([
            7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112, 7.1095, 7.1220, 7.1310,
            7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415, 7.1445, 7.1525, 7.1440,
            7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220, 7.1230, 7.1225, 7.1180,
            7.1250, 7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235, 7.1645, 7.1565,
            7.1560,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 2;
        let atr = atr(&high, &low, &close, atr_period, Some("SMMA"));

        let factor = 3.0;
        let expected_supertrend = vec![
            7.0435004, 7.0435004, 7.0435004, 7.054437, 7.075719, 7.080235, 7.080235, 7.080235,
            7.080235, 7.080235, 7.080235, 7.080235, 7.1008663, 7.1008663, 7.105092, 7.1122966,
            7.115898, 7.1175737, 7.1175737, 7.1175737, 7.1175737, 7.1175737, 7.1175737, 7.1175737,
            7.1175737, 7.1175737, 7.1175737, 7.158781, 7.158781, 7.158781, 7.158781, 7.157001,
            7.152126, 7.1466875, 7.1466875, 7.1466875, 7.1466875, 7.1466875, 7.1466875, 7.1466875,
            7.1466875, 7.1466875, 7.1074786, 7.1074786, 7.1074786,
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0,
        ];

        let (direction, supertrend) = supertrend(&hl2, &close, &atr, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_supertrend: Vec<f32> = supertrend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_supertrend, expected_supertrend);
        assert_eq!(result_direction, expected_direction);
    }
}
