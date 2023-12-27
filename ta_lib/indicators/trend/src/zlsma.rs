use core::prelude::*;

pub fn zlsma(source: &Series<f32>, period: usize) -> Series<f32> {
    let lsma = source.linreg(period);

    2. * &lsma - lsma.linreg(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlsma() {
        let source = Series::from([
            7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112, 7.1095, 7.1220, 7.1310,
            7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415, 7.1445, 7.1525, 7.1440,
            7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220, 7.1230, 7.1225, 7.1180,
            7.1250, 7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235, 7.1645, 7.1565,
            7.1560,
        ]);
        let period = 3;
        let expected = vec![
            0.0, 7.088, 5.925042, 7.1236806, 7.1175256, 7.135417, 7.1420703, 7.1117597, 7.1072783,
            7.1239357, 7.1312175, 7.1539693, 7.1497893, 7.1412854, 7.141484, 7.143811, 7.149786,
            7.15152, 7.1415567, 7.143571, 7.1534204, 7.1443624, 7.135909, 7.1310244, 7.137115,
            7.1262765, 7.117335, 7.114386, 7.127291, 7.1236925, 7.12111, 7.1235223, 7.117843,
            7.1245036, 7.1240044, 7.1124487, 7.1202955, 7.1312103, 7.1337156, 7.131895, 7.116152,
            7.1222796, 7.1652455, 7.1591597, 7.152091,
        ];

        let result: Vec<f32> = zlsma(&source, period).into();

        assert_eq!(result, expected);
    }
}
