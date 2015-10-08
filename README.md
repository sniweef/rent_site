##1. 基本数据结构及数据传输方法
###1.1 铺位信息：Shop类
- shop_number：铺位号，字符串，最长10个字符。
- area：面积，32位整数。
- price：价格，32位整数。
- project_condition：工程条件，字符串，最长50个字符。
- others：其它，这里暂定为填写招商对象，字符串，最长50个字符。
###1.2 招租信息：RentProject类
- _id：招租商铺的ID。它是个ObjectId对象，包含属性\$oid，该属性对应的值是一条由字母数字组成的24字节字符串，每个用户对应的字符串值都不一样。其对应JSON字符串形如:
> "_id": {"\$oid": "5610eb3007f4012ca823ecf7"}

- create_time：datetime对象，对应JSON字符串形如：
> "create_time": {"\$date": 1444336935837}

- is_approved：是否通过审核，只有通过审核的项目才能被搜索到
- is_sell：是出租还是出售，布尔值，true代表出售，false时代表出租。
- pictures：项目概念图数组，由图片URL字符串（最长100个字符）组成的数组。
- brochure：宣传手册URL，最长100个字符。
- project_name：工程名称，最长50个字符。
- project_type：工程类别，整数，1－4分别代表购物中心、步行街、星级酒店、社区商业。
- position：定位，字符串，最长50个字符。
- address：地址，最长50个字符。
- contacter：联系人，最长50个字符。
- phone：联系人电话，字符串，最长50个字符。
- shops_info：铺位信息，为Shop对象组成的数组。
- shops_price：该工程下所有铺位价格组成的数组。
- shops_area：该工程下所有铺位面积组成的数组。
- shops_investment：该工程下所有铺位的招商对象（字符串）组成的数组。
###1.3 求租信息：WantedShop类
- _id：求租帖子的ID，是个ObjectId对象。
- create_time：datetime对象，对应JSON字符串形如：
"create_time": {"$date": 1444336935837}
- is_approved：是否通过审核。只有通过审核的求租信息才会被搜索到。
- is_buy：是否求购，布尔值，true代表求购，false代表出租。
- wanter_type：营运类型，32位整数，1-3分别代表个人、加盟商、公司直营。
- intention_type：意向类型，32位整数， 1-4分别代表购物中心、步行街、星级酒店、社区商业。
- business_type：经营类型，32位整数，1-7分别代表零售、专卖、餐饮、娱乐、生活服务、银行、金融。
- brand_name：品牌名称，字符串，最长10个字符。
- area：需求面积，32位整数。
- intention_price：意向价格，32位整数。
- project_demand：工程需求，字符串，最长50个字符。
- contacter：联系人，最长50个字符。
- phone：联系人电话，字符串，最长50个字符。
###1.4 数据传输方法：
为了便于跨平台使用及后期做web页面的扩展，APP与服务器后台均使用HTTP GET／POST方法来进行通信。另外，对于搜索及查看商铺、求租信息等功能，服务器会返回JSON字符串，其它功能则是简单地返回结果。具体请看第2章。

##2. 招租信息管理
###2.1 发布招租信息
1) 请求方式：因为招租信息中可能包含图片及宣传手册等，所以需要将其分为两个步骤：首先先将图片或宣传手册POST到服务器上（URL：http://IP/resources/，后期会转用七牛服务器），成功后服务器会返回图片的URL数组，APP需要将数组和原有数据一起再POST到服务器上（URL：http://IP/rent/publish）。
	POST资源文件时使用 multipart/form-data 的形式进行上传，可同时POST3张图片。之后APP需要POST以下表单到服务器上（参考RentProject类）：

- is_sell：是否出售。
- pictures-N：之前POST图片时服务器返回的URL，注意，此处的N为图片的编号，从0开始。如已经上传了3张图片，则应该分别将图片URL放到pictures-0/pictures-1/pictures-2这3个元素里面，可参考后面的例子。
- brochure：宣传手册URL。
- project_name：工程名称。
- project_type：工程类别。
- position：定位。
- address：所有地址。
- contacter：联系人。
- phone：联系人电话。
- shops_info-N-shop_number：铺位号。N为铺位的编号，从0开始。
- shops_info-N-area：铺位使用面积。
- shops_info-N-price：铺位价格。
- shops_info-N-project_condition：铺位工程条件。
- shops_info-N-others：铺位其它信息。

2) 返回数据

- POST图片时会返回一个URL数组对应的JSON字符串，如：

> ["http://127.0.0.1:5000/resources/561242bd07f40122adf13173.jpg"]

- POST招租信息表单时若成功会返回该工程的ID字符串，失败则返回400错误，其中HTML正文会包含错误信息。

3) 例子

- POST图片（使用curl工具模拟）

> curl 127.0.0.1:5000/resources -F  'file1=@1.jpg' -F 'file2=@2.jpg'

之后服务器会返回：

> ["http://127.0.0.1:5000/resources/5612456707f40122adf13175.jpg",
> "http://127.0.0.1:5000/resources/561246b307f40122adf13178.jpg"]

- 再POST表单（注意里面的pictures-N字段）：

> curl 127.0.0.1:5000/rent/publish -F
> 'pictures-0=http://127.0.0.1/1.jpg' -F0.0.1/2.jpg' -F 'is_sell=true'
> -F 'project_name=project name' -F 'project_type=3' -F 'address=shenzhen baoan' -F 'contacter=mr huang' -F 'phone=123456' -F
> 'shops_info-0-shop_number=1' -F 'shops_info-0-area=100' -F
> 'shops_info-0-price=1000' -F 'shops_info-0-project_condition=project
> condition' -F 'shops_info-0-others=other words'

之后成功的话服务器会返回类似下面的ID字符串：

> 5614e34007f40175f131553d

失败会返回400错误，并携带对应的出错信息。

###2.2 更新招租信息
1) 请求方式：类似于发布招租信息，分为两部分，更新图片及内容，但目前更新图片没有实现，后面再做讨论。更新内容时也同2.1一样，需要POST整个表单到服务器上（URL：http://IP/rent/publish），除此之外，表单还需要携带以下信息：
id：当前招租帖子的ID字符串，如上面例子里提到的 字符串：5614e34007f40175f131553d。此字符串在访问招租帖子时由服务器返回给APP。
2) 若成功返回200 及ID字符串，表单参数出错会返回400错误并携带错误信息。另外，id不合法或不存在的话会返回404错误。
3) 例子：参考2.1的例子，新加的id参数可以加到curl命令的最后如：

> curl … -F 'id=5611e73707f40110eb0150ff'

###2.3 通过审核招租信息
1) 请求方式：访问URL：http://IP/rent/approve/id（其中id为招租商铺的id字符串，如5611e73707f40110eb0150ff）。注意：只有通过审核的工程信息才能被后面的搜索功能搜索到。
2) 返回数据：成功返回200 OK，否则返回404错误。
###2.4 查看招租信息
1) 请求方式：访问URL：http://IP/rent/view/id（其中id为招租商铺的id字符串，如5611e73707f40110eb0150ff）。
2) 返回数据：如id不存在则返回空对象，即字符串：'{}'，如存在则返回一个JSON对象对应的字符串，该JSON对象包含的属性请参考RentProject类.
3) 例子：使用浏览器访问：http://127.0.0.1:5000/rent/view/561664a707f40109e8d5e6b3，之后在浏览器中可以看到类似以下信息：

> {"_id": {"\$oid": "561664a707f40109e8d5e6b3"}, "create_time":
> {"\$date": 1444336935837}, "is_approved": true, "is_sell": true,
> "pictures": ["http://127.0.0.1/1.jpg", "http://127.0.0.1/2.jpg"],
> "project_name": "project name", "project_type": 1, "position": "",
> "address": "shenzhen baoan", "contacter": "mr huang", "phone":
> "123456", "shops_info": [{"shop_number": "1", "area": 100, "price":
> 1000, "project_condition": "project condition", "others": "other
> words"}], "shops_price": [1000], "shops_area": [100],
> "shops_investment": ["other words"]}

###2.5 删除招租信息
1) 请求方式：访问URL：http://IP/rent/delete/id（id为商铺的id字符串）
2) 返回数据：如成功返回200 OK，id不存在返回404错误。

###2.6 查找招租信息
1) 请求方式：访问URL：http://IP/rent/search?key=%s&from=%d（其中%s为具体要搜索的字符串，%d代表一个数字，如为N则代表返回第N个及之后的数据，N从0开始，不带from参数则默认为0。）目前的搜索算法：可输入多个关键字，第一个关键字可以是地址的某一部分（如深圳市），之后的关键字可以是项目名称的一部分，任何匹配到的结果都会展示出来。
2) 返回数据：返回一个JSON数组（大小暂定为10）。每个数组元素为包含以下数据的对象（参考RentProject类）:

- _id：ObjectId对象。
- project_name：项目名称。
- address：地址。
- shops_price：价格。整数数组。
- shops_area：面积。整数数组。
- shops_investment：招商对象。字符串数组。

3) 例子：
访问URL：http://127.0.0.1:5000/rent/search?key=baoan，得到以下数据：

> [{"project_name": "project name", "_id": {"\$oid":
> "561664a707f40109e8d5e6b3"}, "shops_investment": ["other words"],
> "shops_price": [1000], "address": "shenzhen baoan", "shops_area":
> [100]}, {"project_name": "project name", "_id": {"$oid":
> "561664a707f40109e8d5e6b2"}, "shops_investment": ["other words"],
> "shops_price": [1000], "address": "shenzhen baoan", "shops_area":
> [100]}]

由上可以看到虽然project_name里不包括关键字baoan，但是address字段里有，所以就得到了这两个结果。这里如果搜索project也可以得到上面两个结果。

##3. 求租信息管理
这部分的内容和第2章大同小异，二者不同的地方仅仅是请求的URL及返回的数据类型。
###3.1 发布求租信息
1) 请求方式：将数据POST到服务器上，对应URL为：http://IP/wanted/publish，需要提供以下表单（参考WantedShop类）：

- is_buy：是否购买。
- wanter_type：营运类型。
- intention_type：意向类型。
- business_type：经营类型。
- brand_name：品牌名称。
- area：意向面积。
- intention_price：意向价格。
- project_demand：工程需求。
- contacter：联系人。
- phone：联系方式。

2) 返回数据：成功返回200并携带该求租信息的id字符串。失败返回400错误，正文携带错误信息。
###3.2 更新求租信息
1) 请求方式：与发布求租信息类似，唯一不同的是更新POST上的表单需要包含该求租信息的id字符串。
2) 若成功返回200 及ID字符串，表单参数出错会返回400错误并携带错误信息。另外，id不合法或不存在的话会返回404错误。
###3.3 通过审核求租信息
1) 请求方式：访问URL：http://IP/wanted/approve/id（其中id为求租商铺的id字符串）。注意：只有通过审核的求租信息才能被后面的搜索功能搜索到。
2) 返回数据：成功返回200 OK，否则返回404错误。
###3.4 查看求租信息
1) 请求方式：访问URL：http://IP/wanted/view/id（其中id为求租信息的id字符串）。
2) 返回数据：如id不存在则返回空对象，即字符串：'{}'，如存在则返回一个JSON对象对应的字符串，该JSON对象包含的属性请参考WantedShop类.
3) 例子：
访问URL：http://127.0.0.1:5000/wanted/view/5616689a07f4010a6dcf3ee6，服务器会返回类似以下数据：

> {"_id": {"\$oid": "5616689a07f4010a6dcf3ee6"}, "create_time": {"$date":
> 1444337946803}, "is_approved": true, "is_buy": true, "wanter_type": 1,
> "intention_type": 1, "business_type": 1, "brand_name": "brand name",
> "area": 1000, "intention_price": 1000, "project_demand": "request",
> "contacter": "mr huang", "phone": "12345"}

###3.5 删除求租信息
1) 请求方式：访问URL：http://IP/wanted/delete/id（id为求租信息的id字符串）
2) 返回数据：如成功返回200 OK，id不存在返回404错误。
###3.6 查找求租信息
1) 目前的需求其实是不要求去查找求租信息的，但以后可能需要增加这一功能，故这里还是类似2.6提供一个搜索求租信息的URL：http://IP/wanted/search?key=%s&from=%d，其中key和from的意思与2.6一样。这两个参数都可以为空，此时返回的结果即是查看当前所有的求租信息。
2) 返回数据：返回一个JSON数组（大小暂定为10）。每个数组元素为包含以下数据的对象（参考RentProject类）:

- _id：ObjectId对象。
- is_buy：是否求购。
- wanter_type：营运类型。
- intention_type：意向类型。
- business_type：经营类型。
- brand_name：品牌名称。
- area：意向面积。
