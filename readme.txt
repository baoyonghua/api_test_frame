高德地图的API测试


第一步，申请”Web服务API接口”密钥（Key）；
第二步，拼接HTTP请求URL，第一步申请的Key需作为必填参数一同发送；
第三步，接收HTTP请求返回的数据（JSON或XML格式），解析数据。

详见：https://lbs.amap.com/api/webservice/guide/api/staticmaps/

如果有标注/标签/折线（markers/labels/paths）等覆盖物，则中心点（location）和地图级别（zoom）可选填。
当请求中无location值时，地图区域以包含请求中所有的标注/标签/折线的几何中心为中心点；
如请求中无zoom，地图区域以包含请求中所有的标注/标签/折线为准，系统计算出zoom值。


