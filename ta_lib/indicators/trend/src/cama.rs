use core::prelude::*;

pub fn cama(source: &Price, high: &Price, low: &Price, tr: &Price, period: Period) -> Price {
    let hh = high.highest(period);
    let ll = low.lowest(period);

    let alpha = (hh - ll) / tr.sum(period);

    source.ew(&alpha, source)
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::wtr;

    #[test]
    fn test_cama() {
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
        let expected = vec![
            7.1135, 7.099209, 7.105903, 7.1176147, 7.1188717, 7.1342874, 7.1378927, 7.1228094,
            7.1096625, 7.1199923, 7.126775, 7.1509676, 7.148554, 7.1440263, 7.141863, 7.1433816,
            7.14765, 7.14991, 7.14411, 7.144397, 7.152287, 7.147436, 7.140331, 7.131524, 7.1351757,
            7.128313, 7.120285, 7.1158485, 7.123482, 7.1224785, 7.1228695, 7.12264, 7.119289,
            7.122577, 7.122863, 7.116236, 7.1193237, 7.129515, 7.132675, 7.132184, 7.120414,
            7.1226425, 7.1630764, 7.157433, 7.156123,
        ];
        let period = 2;
        let tr = wtr(&high, &low, &close);

        let result: Vec<Scalar> = cama(&close, &high, &low, &tr, period).into();

        assert_eq!(result, expected);
    }
}
