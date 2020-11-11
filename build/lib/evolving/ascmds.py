# -*- coding: utf-8 -*-

# -- practical
# ---------------------------------------------------------------
asdaemons = """/usr/bin/osascript -e '
-- keep process alive

on loginClient(userid, pwd)
	try
		tell application "同花顺" to quit
		delay 0.25
	end try
	
	tell application "同花顺" to activate
	delay 3 -- wait process start up, can not remove
	tell application "System Events"
		tell process "同花顺"
			try
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to userid
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to pwd
				click button "登 录" of window 1 of application process "同花顺" of application "System Events"
				delay 3 -- Wait for the application to load the data, can not remove
			end try
		end tell
	end tell
end loginClient

on daemons(userid, pwd)
	set delayTimeInterval to 15 -- 15 sec
	repeat
		tell application "System Events" to set isRunning to exists (processes where name is "同花顺")
		if not isRunning then
			loginClient(userid, pwd)
		end if
		delay delayTimeInterval -- every delayInterval sec check again
	end repeat
end daemons

on run {userid, pwd}
	-- set userid to "xxxx"
	-- set pwd to "xxxx"
	daemons(userid, pwd)
	
	-- ex
	-- nohup osascript daemons.scpt xxxx xxxx >> /dev/null 2>&1 &
end run
'"""

asisClientLoggedIn = """/usr/bin/osascript -e '
-- is client logged in

on isClientLoggedIn()
	tell application "System Events"
		tell application "System Events" to set isRunning to exists (processes where name is "同花顺")
		if isRunning then
			tell application "同花顺" to activate
			delay 4
			tell process "同花顺"
				-- button "忘记密码" of window 1 of application process "同花顺" of application "System Events"
				-- checkbox "记住密码" of window 1 of application process "同花顺" of application "System Events"
				-- button "游客登录" of window 1 of application process "同花顺" of application "System Events"
				-- button "注册账号" of window 1 of application process "同花顺" of application "System Events"
				-- button "登 录" of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				set val to get value of attribute "AXTitle" of button of window 1 of application process "同花顺" of application "System Events"
				
				if val contains "游客登录" then
					return false
				end if
				
				return true
			end tell
		end if
		-- return isRunning
	end tell
end isClientLoggedIn

isClientLoggedIn()
-- ex
-- osascript isClientLoggedIn.scpt
'"""


asisBrokerLoggedIn = """/usr/bin/osascript -e '
-- is broker logged in

on isBrokerLoggedIn()
	tell application "同花顺" to activate
	delay 0.8
	tell application "System Events"
		tell process "同花顺"
			-- exit if exists
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "模拟" of window 1 of application process "同花顺" of application "System Events" -- 刷新
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			try
				set info to get value of attribute "AXTitle" of button of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				-- {"反馈", "退出"}
			on error
				-- set info to get {"反馈", "退出"} 失败时会产生错误, 说明此时处于未登陆状态
				return false
			end try
			
			if info contains "退出" then
				return true
			else
				return false
			end if
		end tell
	end tell
end isBrokerLoggedIn

isBrokerLoggedIn()
-- ex
-- osascript isBrokerLoggedIn.scpt
'"""


asloginClient = """/usr/bin/osascript -e '
-- login client

on loginClientHelp(userid, pwd)
	try
		tell application "同花顺" to quit
		delay 1
	end try
	
	tell application "同花顺" to activate
	delay 3 -- wait process start up, can not remove
	tell application "System Events"
		tell process "同花顺"
			try
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to userid
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to pwd
				click button "登 录" of window 1 of application process "同花顺" of application "System Events"
				delay 10 -- Wait for the application to login and load data, can not remove
			end try
		end tell
	end tell
end loginClientHelp

on loginClient(userid, pwd)
	set isRunning to false
	repeat 3 times
		tell application "System Events" to set isRunning to exists (processes where name is "同花顺")
		if not isRunning then
			loginClientHelp(userid, pwd)
			tell application "System Events" to set isRunning to exists (processes where name is "同花顺")
		end if
		
		if isRunning then
			exit repeat
		end if
	end repeat
	
	-- return status
	if isRunning then
		return "successed"
	else
		return "failed"
	end if
end loginClient

on run {userid, pwd}
	-- set userid to "xxxx"
	-- set pwd to "xxxx"
	loginClient(userid, pwd)
	
	-- ex
	-- osascript loginClient.scpt userid password
end run
'"""


aslogoutClient = """/usr/bin/osascript -e '
-- logout client

on logoutClient()
	try
		tell application "同花顺" to quit
		return "successed"
	on error
		return "failed"
	end try
end logoutClient

logoutClient()
-- ex
-- osascript logoutClient.scpt
'"""


asloginBroker = """/usr/bin/osascript -e '
-- login broker

on loginBroker(broker_code, trade_account, trade_pwd)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			--> 交易
			-- entire contents
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			try
				set info to get value of attribute "AXTitle" of button of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				-- {"反馈", "退出"}
				if info contains "退出" then
					return "successed"
				end if
			on error
				-- set info to get {"反馈", "退出"} 失败时会产生错误, 说明此时处于未登陆状态
				
				try
					--  交易->立即登录
					click button "立即登录" of window 1 of application process "同花顺" of application "System Events"
					
					-- 交易 -> 立即登录 -> 证券公司
					-- can be user defined !!!. no limit for broker
					-- Todo: add brokers
					-- click button "添加" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					-- 交易 -> 立即登录 -> 证券公司 -> 选择券商 - 需要事先登陆一遍
					click button 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					set brokerName to "平安证券" -- default broker
					
					-- 中信证券
					if broker_code is "ZXZQ" then
						set brokerName to "中信证券"
					-- 平安证券
					else if broker_code is "PAZQ" then
						set brokerName to "平安证券"
					-- 浙商证券
					else if broker_code is "ZSZQ" then
						set brokerName to "浙商证券"
					-- 国泰君安
					else if broker_code is "GTJA" then
						set brokerName to "国泰君安"
					-- 国金证券
					else if broker_code is "GJZQ" then
						set brokerName to "国金证券"
					-- 兴业证券
					else if broker_code is "XYZQ" then
						set brokerName to "兴业证券"
					-- 中金证券
					else if broker_code is "ZJZQ" then
						set brokerName to "中金证券"
					-- 中泰证券
					else if broker_code is "ZTZQ" then
						set brokerName to "中泰证券"
					end if
					
					-- 获取曾经登陆过的券商列表
					set historyBrokers to get value of text field of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					if historyBrokers is {} then
						return "failed" -- please login in manually first
					end if
					if historyBrokers contains brokerName then
						repeat with rowNum from 1 to length of historyBrokers
							set theCurrentListItem to item rowNum of historyBrokers
							if theCurrentListItem contains brokerName then
								-- find rowNum
								exit repeat
							end if
						end repeat
					else
						-- not found
						return "failed" -- please login in manually first
					end if
					
					-- select what you find
					select text field rowNum of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click text field rowNum of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					-- cliclick
					-- get position of rowNum th row
					set po to get position of text field rowNum of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set po1 to get item 1 of po
					set po2 to get item 2 of po
					
					-- duble click this row
					-- note: brew install cliclick
					-- 一定要写全路径 /usr/local/bin/cliclick, 不然失败, 没环境变量
					-- return "/usr/local/bin/cliclick c:" & po1 & "," & po2
					do shell script "/usr/local/bin/cliclick c:" & po1 & "," & po2
					
					delay 0.25
					-- 交易 -> 立即登录 -> 交易账户
					set value of checkbox 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events" to trade_account
					
					-- 交易 -> 立即登录 -> 交易密码
					set value of text field 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events" to trade_pwd
					
					-- 交易 -> 立即登录 -> 验证码
					-- method 0: 验证码直接提取
					set verificationCodeList to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					--static text "5" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					--static text "9" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					--static text "7" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					--static text "2" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					--static text "6" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set verificationCode to ""
					repeat with x from 8 to 12
						set verificationCode to verificationCode & item x of verificationCodeList
					end repeat
					-- return verificationCode
					
					-- method 1: 验证码自动识别，需要传入 model_path 变量，因采用了其他方法，所以已去，暂保留以备不时之需
					-- set model_path to "/Users/star/mmodels"
					-- do shell script "screencapture /tmp/1.png"
					-- set verificationCode to (do shell script "sh " & model_path & "/mmodels/Tservice/instructions/orc.sh " & model_path)
					-- return verificationCode
					
					-- method 2: 验证码手动输入
					-- delay 0.8 -- give user time to memorize verification code
					-- set verificationCode to the text returned of (display dialog "Pls enter verification code" buttons {"No", "Yes"} default button "Yes" default answer "")
					
					-- fill with verificationCode
					set value of text field 2 of sheet 1 of window 1 of application process "同花顺" of application "System Events" to verificationCode
					
					--  交易 -> 立即登录 -> 登录
					click button "登录" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- return entire contents
					
					try
						delay 2 -- 如网络问题，需要delay一段时间才会弹出对话框, delay 时间视机器性能而定, mac pro 2s, 事实上此时是成功的，所以不做 return 处理
						-- static text "连接委托主站失败！可能是以下原因：" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						-- static text "(1) 计算机没有连接到互联网；
						-- (2) 通过代理上网，代理设置不正确；
						-- (3) 防火墙阻挡了通讯；
						-- (4) 营业部的IP地址或域名设置不正确" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						-- button "确定" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						set warningFlag to item 1 of info
						if warningFlag is "连接委托主站失败！可能是以下原因：" then
							click button "确定" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
							-- return "successed"
						end if
					end try
					
					-- 验证码填写方式为直接采集: 不可能出现验证码错误, 故注释, 验证码方式发生改变时再解除注释
					-- try
					---- static text "警告" of sheet 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					---- static text "验证码错误" of sheet 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					---- click button "确认" of sheet 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- set warningFlag to get value of static text of sheet 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- if warningFlag is {"警告", "验证码错误"} then
					-- click button "确认" of sheet 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- return "failed"
					-- end if
					-- end try
					return "successed"
				on error
					return "failed"
				end try
			end try
		end tell
	end tell
end loginBroker

on run {broker_code, trade_account, trade_pwd}
	
	-- set broker to "PAZQ"
	-- set trade_account to "xxxx"
	-- set trade_pwd to "xxxx"
	loginBroker(broker_code, trade_account, trade_pwd)
	
	-- ex
	-- osascript loginBroker.scpt PAZQ xxxx xxxx
end run
'"""


aslogoutBroker = """/usr/bin/osascript -e '
-- logout broker

on logoutBroker()
	tell application "同花顺" to activate
	delay 0.25
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				-- entire contents
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				delay 0.25
				--  交易-> A股 -> 账户设置 退出
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- click button "反馈" of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				click button "退出" of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				-- entire contents
				
				return "successed"
			on error
				return "failed"
			end try
		end tell
	end tell
end logoutBroker

logoutBroker()
-- ex
-- osascript logoutBroker.scpt
'"""


astransfer = """/usr/bin/osascript -e '
-- transfer: bank to broker

-- 需要先手动登陆一遍
on transfer(transferType, amount, bank_pwd, trade_pwd)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events" -- 刷新
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				delay 0.25
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				click button "转账" of UI element 2 of row 9 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				-- click button "流水" of UI element 2 of row 9 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				if transferType is "broker2bank" then
					click button 2 of window "银证转账" of application process "同花顺" of application "System Events"
					set value of text field 1 of window "银证转账" of application process "同花顺" of application "System Events" to amount
					set value of text field 2 of window "银证转账" of application process "同花顺" of application "System Events" to bank_pwd
					set value of text field 3 of window "银证转账" of application process "同花顺" of application "System Events" to trade_pwd
					delay 0.1
					click button "确定转入银行" of window "银证转账" of application process "同花顺" of application "System Events"
				else if transferType is "bank2broker" then
					-- click button 2 of window "银证转账" of application process "同花顺" of application "System Events" -- default
					set value of text field 1 of window "银证转账" of application process "同花顺" of application "System Events" to amount
					set value of text field 2 of window "银证转账" of application process "同花顺" of application "System Events" to bank_pwd
					set value of text field 3 of window "银证转账" of application process "同花顺" of application "System Events" to trade_pwd
					delay 0.1
					click button "确定转入券商" of window "银证转账" of application process "同花顺" of application "System Events"
				end if
				
				-- 您是否确认以上转账信息?" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
				click button "确认" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
				--click button "取消" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
				delay 0.2
				
				try
					-- static text "外部机构[5200]不支持7*24银证业务" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
						click button 6 of window "银证转账" of application process "同花顺" of application "System Events" -- close window
						return {"failed", "警告:外部机构[5200]不支持7*24银证业务"}
					end if
				end try
				
				try
					-- 转账成功后关闭转账窗口
					click button 1 of window "银证转账" of application process "同花顺" of application "System Events"
				end try
				
				return "successed"
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end transfer

on run {transferType, amount, bank_pwd, trade_pwd}
	-- transferType: "bank2broker", "broker2bank"
	-- amount
	-- bank_pwd
	-- trade_pwd
	
	-- set transferType to "broker2bank"
	-- set amount to "100000"
	-- set bank_pwd to "112173"
	-- set trade_pwd to "xxxx"
	transfer(transferType, amount, bank_pwd, trade_pwd)
	
	-- ex
	-- osascript transfer.scpt bank2broker 100 123456 xxxx
end run
'"""


asgetTransferRecords = """/usr/bin/osascript -e '
-- get transfer records

on getTransferRecords(dateRange)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.1
				click button "流水" of UI element 2 of row 9 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				-- static text "委托时间：" of window "查询流水" of application process "同花顺" of application "System Events"
				click button "今天" of window "查询流水" of application process "同花顺" of application "System Events"
				delay 0.2
				
				if dateRange is "today" then
					click button "今天" of pop over 1 of window "查询流水" of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window "查询流水" of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window "查询流水" of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window "查询流水" of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window "查询流水" of application process "同花顺" of application "System Events"
				end if
				
				delay 0.01
				set info to get value of static text of every row of table 1 of scroll area 1 of window "查询流水" of application process "同花顺" of application "System Events"
				set comment to get value of attribute "AXTitle" of every button of group 1 of table 1 of scroll area 1 of window "查询流水" of application process "同花顺" of application "System Events"
				
				-- close window
				click button 1 of window "查询流水" of application process "同花顺" of application "System Events"
				return {"successed", comment, info}
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getTransferRecords

on run {dateRange}
	-- range: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear" 
	
	-- set dateRange to "thisYear"
	getTransferRecords(dateRange)
	
	-- ex
	-- osascript getTransferRecords.scpt thisWeek
end run
'"""


asgetBids = """/usr/bin/osascript -e '
-- get account information

on getBids(assetType, stockCode)
	tell application "同花顺" to activate
	delay 0.25
	tell application "System Events"
		tell process "同花顺"
			--> 交易
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "模拟" of window 1 of application process "同花顺" of application "System Events" -- 刷新
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			
			--> 交易 -> 股票
			if assetType is "stock" then
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
			else if assetType is "sciTech" then
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
			else if assetType is "gem" then
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
			else
				return {"failed", "wrong option: " & assetType}
			end if
			
			try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode -- 先输入, 等待加载数据
				
				click button "卖出" of window 1 of application process "同花顺" of application "System Events" -- 刷新
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				delay 0.1
				set bidsSPrice to get value of attribute "AXTitle" of every button of every UI element of every row of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				
				set bidsBPrice to get value of attribute "AXTitle" of every button of every UI element of every row of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events"
				
				set bidsS_vol to get value of every static text of every UI element of every row of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				
				set bidsB_vol to get value of every static text of every UI element of every row of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events"
				
				return {"successed", bidsSPrice, bidsBPrice, bidsS_vol, bidsB_vol}
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getBids

on run {assetType, stockCode}
	-- assetType: "stock", "sciTech", "gem"
	-- stockCode
	
	-- set assetType to "stock"
	-- set stockCode to "600030"
	
	-- set assetType to "sciTech"
	-- set stockCode to "688055"
	
	-- set assetType to "gem"
	-- set stockCode to "300750"
	
	getBids(assetType, stockCode)
	
	-- ex
	-- osascript getBids.scpt stock 600030
end run
'"""


asissuingEntrust = """/usr/bin/osascript -e '
-- issuing trading action

on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				--> 交易 -> 股票
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				-- 交易前委托状态
				------------------------------------------------
				click button "持仓" of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				
				--选择委托时间 -> 今天 - 弹出时间选择
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				
				-- 显示当日所有委托
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				
				-- sometimes in area 4 sometimes in area 5
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				-- 进行交易委托
				------------------------------------------------
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode -- 先填写一次, 后面再填写一次, 让它提前加载数据
				if tradingAction is "buy" then
					click button "卖出" of window 1 of application process "同花顺" of application "System Events" -- 来回刷新一下，刷出 bids 列表
					click button "买入" of window 1 of application process "同花顺" of application "System Events"
				else if tradingAction is "sell" then
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
					click button "买入" of window 1 of application process "同花顺" of application "System Events"
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				end if
				-- cursor needs to be activated before input stock code
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				
				-- 如果成功率还是低, 那么直接设置为涨跌停价
				-- 如未设定价格, 则给price重新赋值, 买时设置为卖5, 卖时设置为买5，会以最优买时为 卖1，卖时为 买1成交: 成交规则: 价, 时, 量字典序
				if price is "None" then
					delay 0.05 -- 需要delay
					if tradingAction is "buy" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events") -- 卖5价
						if price is "- -" then -- 涨停时卖一价不存在, 设置为买一价, 也即涨停价
							set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events") -- 买1价
						end if
					else if tradingAction is "sell" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events") -- 买5价
						if price is "- -" then -- 跌停时买一价不存在, 设置为卖一价, 也即跌停价
							set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events") -- 卖1价
						end if
					end if
				end if
				
				delay 0.25 -- 需要delay, 不然无法输入, 永远以最优价成交: 视机器性能优化, mac pro 尽量 0.25 以上
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				
				if tradingAction is "buy" then
					click button "确定买入" of window 1 of application process "同花顺" of application "System Events"
				else if tradingAction is "sell" then
					click button "确定卖出" of window 1 of application process "同花顺" of application "System Events"
				end if
				
				
				-- gem 创业版盘后特殊
				-- static text "提示信息" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- static text "股东账号:0277525271
				-- 证券代码:300474
				-- 买入价格:75.45
				-- 买入数量:100
				-- 您是否确认以上买入委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "提示信息" then
						delay 0.01
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					end if
				end try
				
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"买入委托"} or info contains {"卖出委托"} then
					-- 确认委托
					-- static text "买入委托" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "股东账号:
					-- 券代码:002241
					-- 入价格:37.01
					-- 入数量:100
					-- 是否确认以上买入委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					-- static text "卖出委托" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "股东账号:
					-- 证券代码:600703
					-- 卖出价格:27.26
					-- 卖出数量:100
					-- 您是否确认以上卖出委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					-- 确认委托
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				-- 其实如下信息可简化为一条 contains
				--	if info contains {"警告", "资金可用数不足"} then
				--		-- 错误 1
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "资金可用数不足" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 1
				--	else if info contains {"警告", "用于交易的股份不足"} then
				--		-- 错误 2
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "用于交易的股份不足" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 2
				--	else if info contains {"警告", "委托价超过涨跌幅"} then
				--		-- 错误 3
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "委托价超过涨跌幅" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 3
				--	else if info contains {"警告", "请输入正确的委托价格!"} then
				--		-- 错误 4
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "请输入正确的委托价格!" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 4
				--	else if info contains {"警告", "请输入正确的证券代码!"} then
				--		-- 错误 5
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "请输入正确的证券代码!" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 5
				--	else if info contains {"警告", "暂时无法办理此项业务您可以稍后再试，敬请谅解"} then
				--		-- 错误 6
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "暂时无法办理此项业务您可以稍后再试，敬请谅解" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 6
				--	else if info contains {"警告", "业务提示:[不符合交易所零股卖出规则]"} then
				--		-- 错误 7
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "业务提示:[不符合交易所零股卖出规则]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 7
				--	else if info contains {"警告"} then -- 其他告警
				--		-- 错误 8
				--		-- {"警告", "股份信息[加载:325319118391, 0277525271, 2241, 0, 007056]不存在"}
				--		set flag to 8
				--	end if
				
				if info contains {"警告"} then
					set flag to -1
				end if
				
				-- close warning
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				
				-- 交易后委托状态
				------------------------------------------------
				click button "持仓" of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				
				--选择委托时间 -> 今天 - 弹出时间选择
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				
				-- 显示当日所有委托
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				
				delay 0.6 -- 成功时等待其加入委托列表 -- 买入组合时这个时间不能再减少，会导致无法输出 contractNo
				-- sometimes in area 4 sometimes in area 5
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				set contractNoList to {} -- contractNoList2 - contractNoList1
				set contractNoList1 to {} -- 交易发起前委托合同号列表
				set contractNoList2 to {} -- 交易发起后委托合同号列表
				repeat with x from 1 to length of revocableEntrustment1
					set end of contractNoList1 to item 11 of item x of revocableEntrustment1
				end repeat
				repeat with x from 1 to length of revocableEntrustment2
					set end of contractNoList2 to item 11 of item x of revocableEntrustment2
				end repeat
				repeat with x from 1 to length of contractNoList2
					set curitem to item x of contractNoList2
					if contractNoList1 does not contain curitem then
						set end of contractNoList to curitem
					end if
				end repeat
				
				if contractNoList is {} then
					set info to "委托失败"
					return {"failed", "委托失败"}
				else
					return {"successed", contractNoList}
				end if
				
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end issuingEntrust

on run {tradingAction, assetType, stockCode, price, amount}
	-- tradingAction: "buy", "sell"
	-- assetType: "stock", "sciTech", "gem"
	-- stockCode:
	-- price: None
	-- amount:
	
	-- set tradingAction to "sell"
	-- set assetType to "stock"
	-- set stockCode to "601012"
	-- set price to "37.01"
	-- set price to "None"
	-- set amount to "100"
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	
	-- ex
	-- osascript issuingEntrust.scpt buy stock 002241 37.01 100
end run
'"""


asrevokeEntrust = """/usr/bin/osascript -e '
-- revoke entrust

on revokeEntrust(revokeType, assetType, contractNo)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.2
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				delay 0.2
				
				if revokeType is "allBuyAndSell" then
					click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "allBuy" then
					click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "allSell" then
					click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "contractNo" then
					-- select static text "N8743630" of row 2 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					
					-- get row num of the contractNo
					-- sometimes in area 4 sometimes in area 5
					set idarea to 4
					try
						set EntrustmentList to get value of static text of row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					on error
						set idarea to 5
						set EntrustmentList to get value of static text of row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					end try
					
					if EntrustmentList is {} then
						return {"successed", "nothing to revoke"}
					end if
					repeat with rowNum from 1 to length of EntrustmentList
						set theCurrentListItem to item rowNum of EntrustmentList
						if theCurrentListItem contains contractNo then
							exit repeat
						end if
					end repeat
					set len to length of EntrustmentList
					if rowNum is len then
						if theCurrentListItem does not contain contractNo then
							-- not found
							return {"successed", "contract No. " & contractNo & " was not found"}
						end if
					end if
					
					-- get position of rowNum th row
					if idarea is 4 then
						set po to get position of (get item 11 of (get static text of row rowNum of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"))
					else if idarea is 5 then
						set po to get position of (get item 11 of (get static text of row rowNum of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"))
					end if
					set po1 to get item 1 of po
					set po2 to get item 2 of po
					
					-- duble click this row
					-- note: brew install cliclick
					-- return "cliclick dc:" & po1 & "," & po2
					do shell script "/usr/local/bin/cliclick dc:" & po1 & "," & po2
				end if
				
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", "revoke " & revokeType & " " & assetType & " is successed"}
				on error
					return {"successed", "nothing to revoke"}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end revokeEntrust

on run {revokeType, assetType, contractNo}
	-- revokeType: "allBuy", "allSell", "allBuyAndSell", "contractNo"
	-- assetType: "stock", "sciTech"
	-- contractNo: specify a contractNo, ex. "JHZOCGQV"
	
	-- set revokeType to "contractNo"
	-- set assetType to "stock"
	-- set contractNo to "JHZOCGQV"
	
	revokeEntrust(revokeType, assetType, contractNo)
	
	-- ex
	-- osascript revokeEntrust.scpt allBuyAndSell stock None
end run
'"""


asrevokeAllEntrust = """/usr/bin/osascript -e '
-- revoke all entrust

on revokeAllEntrust()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				return {"successed"}
				
				-- click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				-- click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				-- click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				
				-- static text "撤单委托" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- static text "您确定要撤销这3笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
			on error
				return {"failed"}
			end try
		end tell
	end tell
end revokeAllEntrust

revokeAllEntrust()
-- ex
-- osascript revokeAllEntrust.scpt
'"""


asrevokeAllBuyEntrust = """/usr/bin/osascript -e '
-- revoke all buy entrust

on revokeAllBuyEntrust()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				return {"successed"}
				
				-- click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				-- click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				-- click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
			on error
				return {"failed"}
			end try
		end tell
	end tell
end revokeAllBuyEntrust

revokeAllBuyEntrust()
-- ex
-- osascript revokeAllBuyEntrust.scpt
'"""


asrevokeAllSellEntrust = """/usr/bin/osascript -e '
-- revoke all sell entrust

on revokeAllSellEntrust()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"					
				end try
				return {"successed"}
				
				-- click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				-- click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				-- click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
			on error
				return {"failed"}
			end try
		end tell
	end tell
end revokeAllSellEntrust

revokeAllSellEntrust()
-- ex
-- osascript revokeAllSellEntrust.scpt
'"""


asgetAccountInfo = """/usr/bin/osascript -e '
-- get account information

on getAccountInfo()
	tell application "同花顺" to activate
	delay 0.5 -- 不可再减少
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				delay 0.5
				tell table 1 of scroll area 1 of window 1
					set accountInfo to get value of every static text of every UI element of every row of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", accountInfo}
				end tell
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getAccountInfo

getAccountInfo()
-- ex
-- osascript getAccountInfo.scpt
'"""


asgetHoldingShares = """/usr/bin/osascript -e '
-- get holding shares

on getHoldingShares(assetType)
	tell application "同花顺" to activate
	delay 0.5 -- 不可再减少
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.1
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				-- click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				-- sometimes in area 4 sometimes in area 5
				delay 0.1
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set holdingShares to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set holdingShares to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				return {"successed", comments, holdingShares}
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getHoldingShares

on run {assetType}
	-- assetType: "stock", "sciTech"
	
	-- set assetType to "stock"
	getHoldingShares(assetType)
	
	-- ex
	-- osascript getHoldingShares.scpt stock
end run
'"""


asgetEntrust = """/usr/bin/osascript -e '
-- get entrust

on getEntrust(assetType, dateRange, isRevocable)
	tell application "同花顺" to activate
	delay 0.5 -- 不可再减少
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 先点自选归位状态
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.5
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				click button "持仓" of window 1 of application process "同花顺" of application "System Events" -- 归位
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				--选择委托时间 -> 今天 - 弹出时间选择
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				
				-- 选择委托时间
				if dateRange is "today" then
					click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				delay 0.1
				
				-- 只显示可撤销委托
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if isRevocable is "true" then
						if checkboxStatus is false then click theCheckbox
					else -- else uncheck theCheckbox when isRevocable is false
						if checkboxStatus is true then click theCheckbox
					end if
				end tell
				
				-- return entire contents
				-- sometimes in area 4 sometimes in area 5
				
				try
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				try
					-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "业务提示:[开始日期(2020-01-01) - 结束日期(2020-08-03) 超过 93 天]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", {"警告"}, {"业务提示: 超过 93 天"}}
					end if
					return {"successed", comments, revocableEntrustment}
				on error
					return {"successed", comments, revocableEntrustment}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getEntrust

on run {assetType, dateRange, isRevocable}
	-- assetType: "stock", "sciTech"
	-- dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
	-- isRevocable: true, false
	
	-- set assetType to "stock"
	-- set dateRange to "today"
	-- set isRevocable to "false"
	getEntrust(assetType, dateRange, isRevocable)
	
	-- ex
	-- osascript getEntrust.scpt stock thisWeek false
end run
'"""


asgetClosedDeals = """/usr/bin/osascript -e '
-- get closed deals

on getClosedDeals(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5 -- 不可再减少
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.5
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				click button "成交" of window 1 of application process "同花顺" of application "System Events"
				-- click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				-- 成交时间
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				
				if dateRange is "today" then
					click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				delay 0.45
				
				-- return entire contents				
				-- sometimes in area 4 sometimes in area 5
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				try
					-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "业务提示:[开始日期(2020-01-01) - 结束日期(2020-08-03) 超过 93 天]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", "警告, 业务提示: 超过 93 天"}
					end if
					return {"successed", comments, closedDeals}
				on error
					return {"successed", comments, closedDeals}
				end try
				
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getClosedDeals

on run {assetType, dateRange}
	-- assetType: "stock", "sciTech"
	-- dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
	
	-- set assetType to "stock"
	-- set dateRange to "thisSeason"
	
	getClosedDeals(assetType, dateRange)
	
	-- ex
	-- osascript getClosedDeals.scpt stock thisYear
end run
'"""


asgetCapitalDetails = """/usr/bin/osascript -e '
-- get capital details

on getCapitalDetails(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5 -- 不可再减少
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.5
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				-- click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				-- 成交时间
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				
				if dateRange is "today" then
					click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				delay 0.1
				
				-- return entire contents	
				-- sometimes in area 4 sometimes in area 5
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					-- set closedDeals to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every text field of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					-- set closedDeals to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every text field of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				try
					-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "业务提示:[开始日期(2020-01-01) - 结束日期(2020-08-03) 超过 93 天]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", {"警告"}, {"业务提示: 超过 93 天"}}
					end if
					return {"successed", comments, closedDeals}
				on error
					return {"successed", comments, closedDeals}
				end try
				
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getCapitalDetails

on run {assetType, dateRange}
	-- assetType: "stock", "sciTech"
	-- dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
	
	-- set assetType to "stock"
	-- set dateRange to "thisSeason"
	
	getCapitalDetails(assetType, dateRange)
	
	-- ex
	-- osascript getCapitalDetails.scpt stock thisSeason
end run
'"""


asgetIPO = """/usr/bin/osascript -e '
on getIPO(queryType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 刷新一下, 不然选择的时间范围为上一次
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				--> 交易 -> 新股申购
				click button "新股申购" of window 1 of application process "同花顺" of application "System Events"
				-- delay 1 -- 打新时不能再减少了, 需要等待加载数据, 查询时可注释
				
				-- button "证券名称" of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- button "申购代码" of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- button "可申购数量" of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- button "申购数量" of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- static text "今日新股" of window 1 of application process "同花顺" of application "System Events"
				-- scroll area 3 of window 1 of application process "同花顺" of application "System Events"
				-- text area 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events"
				
				-- set CommentTodayNew to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- set rules to get get value of text area 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events"				
				-- 数据暂时未提取，当天无数据
				
				if queryType is "entrust" then
					click button "申购委托" of window 1 of application process "同花顺" of application "System Events"
				else if queryType is "allotmentNo" then
					click button "配号查询" of window 1 of application process "同花顺" of application "System Events"
				else if queryType is "winningLots" then
					click button "中签查询" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "have no " & queryType & "queryType"}
				end if
				
				if queryType is not "entrust" then
					click button "今天" of window 1 of application process "同花顺" of application "System Events"
					if dateRange is "today" then
						click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
					else if dateRange is "thisWeek" then
						click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
					else if dateRange is "thisMonth" then
						click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
					else if dateRange is "thisSeason" then
						click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
					else if dateRange is "thisYear" then
						click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
					end if
				else
					if dateRange is not "today" then
						return {"failed", "<queryType> entrust only supports <dateRange> today"}
					end if
				end if
				
				-- Note: queryType: entrust, allotmentNo, winningLots 的 comment 均不同, 返回到 python 再处理
				set comment to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				set res to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				
				return {"successed", comment, res}
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getIPO

on run {queryType, dateRange}
	-- queryType: entrust, allotmentNo, winningLots
	-- dateRange: today, thisWeek, thisMonth, thisSeason, thisYear
	
	-- set queryType to "winningLots"
	-- set dateRange to "thisMonth"
	getIPO(queryType, dateRange)
	
	-- ex
	-- osascript getIPO.scpt allotmentNo thisWeek
end run
'"""


asgetTodayIPO = """/usr/bin/osascript -e '
on getTodayIPO()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 刷新一下, 不然选择的时间范围为上一次
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				--> 交易 -> 新股申购
				click button "新股申购" of window 1 of application process "同花顺" of application "System Events"
				delay 1.2 -- 打新时不能再减少了, 需要等待加载数据
				
				-- rules 申购规则
				-- set rules to get get value of text area 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events"
				set comment to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				
				-- UI element "广汇发债" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- checkbox 1 of UI element "广汇发债" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- static text "广汇发债" of UI element "广汇发债" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- UI element "733297" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- static text "733297" of UI element "733297" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- UI element "0" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- static text "0" of UI element "0" of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- UI element 4 of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- text field 1 of UI element 4 of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				-- row 2 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				
				set todayipo to get value of static text of UI element of row of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				set nums to get value of text field 1 of UI element 4 of row of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
				repeat with idx from 1 to length of nums
					set curItem to item idx of nums
					set item 4 of item idx of todayipo to curItem
				end repeat
				return {"successed", comment, todayipo}
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getTodayIPO

getTodayIPO()
-- ex
-- osascript todayIPO.scpt
'"""


asoneKeyIPO = """/usr/bin/osascript -e '
on oneKeyIPO()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				-- click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				--> 交易 -> 新股申购
				click button "新股申购" of window 1 of application process "同花顺" of application "System Events"
				delay 1 -- 不能再减少了, 需要等待加载数据
				--> 交易 -> 新股申购 -> 一键申购
				click button "一键申购" of window 1 of application process "同花顺" of application "System Events"
				-- todo: 还需处理
				-- 打新成功后，点击确定？-- 未完全测试完成
				
				try
					-- static text "请输入正确的委托数量!" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- return info
					if info contains "警告" then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", "请输入正确的委托数量"}
					end if
				end try
				
				return "successed"
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end oneKeyIPO

oneKeyIPO()
-- ex
-- osascript oneKeyIPO.scpt
'"""


# -- simulation
# ---------------------------------------------------------------
asgetAccountInfoSim = """/usr/bin/osascript -e '
-- get account information - simulation

on getAccountInfoSim()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events" -- 刷新
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				delay 0.6
				tell table 1 of scroll area 1 of window 1
					set simulationAccountInfo to get value of every static text of every UI element of every row of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", simulationAccountInfo}
				end tell
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getAccountInfoSim

getAccountInfoSim()
-- ex
-- osascript getAccountInfoSim.scpt
'"""


asissuingEntrustSim = """/usr/bin/osascript -e '
-- issuing trading action simulation

on issuingEntrustSim(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				-- click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				--> 交易 -> 股票
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				-- 交易前委托状态
				------------------------------------------------
				click button "持仓" of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				
				--选择委托时间 -> 今天 - 弹出时间选择
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				
				-- 显示当日所有委托
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				
				-- sometimes in area 4 sometimes in area 5
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				-- 进行交易委托
				------------------------------------------------
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode -- 先填写一次, 后面再填写一次, 让它提前加载数据
				if tradingAction is "buy" then
					click button "卖出" of window 1 of application process "同花顺" of application "System Events" -- 来回刷新一下，刷出 bids 列表
					click button "买入" of window 1 of application process "同花顺" of application "System Events"
				else if tradingAction is "sell" then
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
					click button "买入" of window 1 of application process "同花顺" of application "System Events"
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				end if
				-- cursor needs to be activated before input stock code
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				
				-- 如果成功率还是低, 那么直接设置为涨跌停价
				-- 如未设定价格, 则给price重新赋值, 买时设置为卖5, 卖时设置为买5，会以最优买时为 卖1，卖时为 买1成交: 成交规则: 价, 时, 量字典序
				if price is "None" then
					delay 0.05 -- 需要delay
					if tradingAction is "buy" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events") -- 卖5价
						if price is "- -" then -- 涨停时卖一价不存在, 设置为买一价, 也即涨停价
							set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events") -- 买1价
						end if
					else if tradingAction is "sell" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events") -- 买5价
						if price is "- -" then -- 跌停时买一价不存在, 设置为卖一价, 也即跌停价
							set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events") -- 卖1价
						end if
					end if
				end if
				
				delay 0.25 -- 需要delay, 不然无法输入, 永远以最优价成交: 视机器性能优化, mac pro 尽量 0.25 以上
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				
				if tradingAction is "buy" then
					click button "确定买入" of window 1 of application process "同花顺" of application "System Events"
				else if tradingAction is "sell" then
					click button "确定卖出" of window 1 of application process "同花顺" of application "System Events"
				end if
				
				
				-- gem 创业版盘后特殊
				-- static text "提示信息" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- static text "股东账号:0277525271
				-- 证券代码:300474
				-- 买入价格:75.45
				-- 买入数量:100
				-- 您是否确认以上买入委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "提示信息" then
						delay 0.01
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					end if
				end try
				
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"买入委托"} or info contains {"卖出委托"} then
					-- 确认委托
					-- static text "买入委托" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "股东账号:
					-- 券代码:002241
					-- 入价格:37.01
					-- 入数量:100
					-- 是否确认以上买入委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					-- static text "卖出委托" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "股东账号:
					-- 证券代码:600703
					-- 卖出价格:27.26
					-- 卖出数量:100
					-- 您是否确认以上卖出委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					-- 确认委托
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				-- 其实如下信息可简化为一条 contains
				--	if info contains {"警告", "资金可用数不足"} then
				--		-- 错误 1
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "资金可用数不足" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 1
				--	else if info contains {"警告", "用于交易的股份不足"} then
				--		-- 错误 2
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "用于交易的股份不足" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 2
				--	else if info contains {"警告", "委托价超过涨跌幅"} then
				--		-- 错误 3
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "委托价超过涨跌幅" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 3
				--	else if info contains {"警告", "请输入正确的委托价格!"} then
				--		-- 错误 4
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "请输入正确的委托价格!" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 4
				--	else if info contains {"警告", "请输入正确的证券代码!"} then
				--		-- 错误 5
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "请输入正确的证券代码!" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 5
				--	else if info contains {"警告", "暂时无法办理此项业务您可以稍后再试，敬请谅解"} then
				--		-- 错误 6
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "暂时无法办理此项业务您可以稍后再试，敬请谅解" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 6
				--	else if info contains {"警告", "业务提示:[不符合交易所零股卖出规则]"} then
				--		-- 错误 7
				--		-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		-- static text "业务提示:[不符合交易所零股卖出规则]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				--		set flag to 7
				--	else if info contains {"警告"} then -- 其他告警
				--		-- 错误 8
				--		-- {"警告", "股份信息[加载:xxxx, 0277525271, 2241, 0, 007056]不存在"}
				--		set flag to 8
				--	end if
				
				if info contains {"警告"} then
					set flag to -1
				end if
				
				-- close warning
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				
				-- 交易后委托状态
				------------------------------------------------
				delay 0.25 -- 成功时等待其加入委托列表
				click button "持仓" of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				
				--选择委托时间 -> 今天 - 弹出时间选择
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				
				-- 显示当日所有委托
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				-- sometimes in area 4 sometimes in area 5
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				set contractNoList to {} -- contractNoList2 - contractNoList1
				set contractNoList1 to {} -- 交易发起前委托合同号列表
				set contractNoList2 to {} -- 交易发起后委托合同号列表
				repeat with x from 1 to length of revocableEntrustment1
					set end of contractNoList1 to item 11 of item x of revocableEntrustment1
				end repeat
				repeat with x from 1 to length of revocableEntrustment2
					set end of contractNoList2 to item 11 of item x of revocableEntrustment2
				end repeat
				repeat with x from 1 to length of contractNoList2
					set curitem to item x of contractNoList2
					if contractNoList1 does not contain curitem then
						set end of contractNoList to curitem
					end if
				end repeat
				
				if contractNoList is {} then
					set info to "委托失败"
					return {"failed", "委托失败"}
				else
					return {"successed", contractNoList}
				end if
				
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end issuingEntrustSim

on run {tradingAction, assetType, stockCode, price, amount}
	-- tradingAction: "buy", "sell"
	-- assetType: "stock"
	-- stockCode:
	-- price: None
	-- amount:
	
	-- set tradingAction to "buy"
	-- set assetType to "stock"
	-- set stockCode to "002241"
	-- set price to "37.01"
	-- set price to "None"
	-- set amount to "100"
	issuingEntrustSim(tradingAction, assetType, stockCode, price, amount)
	
	-- ex
	-- osascript issuingEntrustSim.scpt buy stock 002241 37.01 100
end run
'"""


asgetHoldingSharesSim = """/usr/bin/osascript -e '
-- get holding shares - simulation

on getHoldingSharesSim(assetType)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				-- click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.1
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				-- click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				-- sometimes in area 5 sometimes in area 4
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set holdingShares to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", comments, holdingShares}
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set holdingShares to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", comments, holdingShares}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getHoldingSharesSim

on run {assetType}
	-- assetType: "stock"
	
	-- set assetType to "stock"
	getHoldingSharesSim(assetType)
	
	-- ex
	-- osascript getHoldingSharesSim.scpt stock
end run
'"""


asgetEntrustSim = """/usr/bin/osascript -e '
-- get entrustment  - simulation

on getEntrustSim(assetType, dateRange, isRevocable)
	tell application "同花顺" to activate
	delay 0.5 -- 不可再减少
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 先点自选归位状态
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				-- click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.1
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				
				click button "持仓" of window 1 of application process "同花顺" of application "System Events" -- 归位
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				--选择委托时间 -> 今天 - 弹出时间选择
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.1
				
				-- 选择委托时间
				if dateRange is "today" then
					click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				
				-- 只显示可撤销委托
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if isRevocable is "true" then
						if checkboxStatus is false then click theCheckbox
					else -- else uncheck theCheckbox when isRevocable is false
						if checkboxStatus is true then click theCheckbox
					end if
				end tell
				
				try
					-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "不支持历史委托查询" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info is {"警告", "不支持历史委托查询"} then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", info}
					end if
				end try
				
				-- return entire contents
				-- sometime in area 4 sometime in area 5
				try
					-- static text "20200802" of row 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", comments, revocableEntrustment}
				on error
					-- static text "20200802" of row 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", comments, revocableEntrustment}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getEntrustSim

on run {assetType, dateRange, isRevocable}
	-- assetType: "stock"
	-- dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear" -- 有可选项，但同花顺不支持模拟交易下委托历史查询，仅支持今天
	-- isRevocable: true, false
	
	-- set assetType to "stock"
	-- set dateRange to "today"
	-- set isRevocable to "false"
	getEntrustSim(assetType, dateRange, isRevocable)
	
	-- ex
	-- osascript getEntrustSim.scpt stock thisWeek false
end run
'"""


asrevokeEntrustSim = """/usr/bin/osascript -e '
-- revoke entrust - simulation

on revokeEntrustSim(revokeType, assetType, contractNo)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				-- click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.2
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option"}
				end if
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				delay 0.2
				
				if revokeType is "allBuyAndSell" then
					click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "allBuy" then
					click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "allSell" then
					click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "contractNo" then
					-- select static text "N8743630" of row 2 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					
					-- get row num of the contractNo
					-- return entire contents
					-- sometimes in area 4 sometimes in area 5
					set idarea to 4
					try
						set EntrustmentList to get value of static text of row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					on error
						set idarea to 5
						set EntrustmentList to get value of static text of row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					end try
					
					if EntrustmentList is {} then
						return {"successed", "nothing to revoke"}
					end if
					repeat with rowNum from 1 to length of EntrustmentList
						set theCurrentListItem to item rowNum of EntrustmentList
						if theCurrentListItem contains contractNo then
							exit repeat
						end if
					end repeat
					set len to length of EntrustmentList
					if rowNum is len then
						if theCurrentListItem does not contain contractNo then
							-- not found
							return {"successed", "contract No. " & contractNo & " was not found"}
						end if
					end if
					
					-- get position of rowNum th row
					if idarea is 4 then
						set po to get position of (get item 11 of (get static text of row rowNum of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"))
					else if idarea is 5 then
						set po to get position of (get item 11 of (get static text of row rowNum of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"))
					end if
					set po1 to get item 1 of po
					set po2 to get item 2 of po
					
					-- duble click this row
					-- note: brew install cliclick
					do shell script "/usr/local/bin/cliclick dc:" & po1 & "," & po2
				end if
				
				try
					-- static text "您确定要撤销这1笔委托?" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- click button "取消" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					
					return {"successed", "revoke " & revokeType & " " & assetType & " is successed"}
				on error
					return {"successed", "nothing to revoke"}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end revokeEntrustSim

on run {revokeType, assetType, contractNo}
	-- revokeType: "allBuy", "allSell", "allBuyAndSell", "contractNo"
	-- assetType: "stock"
	-- contractNo: specify a contractNo, ex. "N8743678" or None
	
	-- set revokeType to "contractNo"
	-- set assetType to "stock"
	-- set contractNo to "N8743678"
	
	revokeEntrustSim(revokeType, assetType, contractNo)
	
	-- ex
	-- osascript revokeEntrustSim.scpt allBuyAndSell stock None
end run
'"""


asgetClosedDealsSim = """/usr/bin/osascript -e '
-- get closed deals - simulation

on getClosedDealsSim(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				
				-- click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				-- delay 0.1
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				
				-- click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				click button "成交" of window 1 of application process "同花顺" of application "System Events"
				-- click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				-- 成交时间
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				
				if dateRange is "today" then
					click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				delay 0.1
				
				-- return entire contents
				-- sometimes in area 4 sometimes in area 5
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				try
					-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "业务提示: 查询时间区间必须在30天以内]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", {"警告, 业务提示: 查询时间区间必须在30天以内"}}
					end if
					return {"successed", comments, closedDeals}
				on error
					return {"successed", comments, closedDeals}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getClosedDealsSim

on run {assetType, dateRange}
	-- assetType: "stock"
	-- dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
	
	-- set assetType to "stock"
	-- set dateRange to "thisWeek"
	
	getClosedDealsSim(assetType, dateRange)
	
	-- ex
	-- osascript getClosedDealsSim.scpt stock thisYear
end run
'"""


asgetCapitalDetailsSim = """/usr/bin/osascript -e '
-- get capital details - simulation

on getCapitalDetailsSim(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				--> 交易
				click button 1 of window 1 of application process "同花顺" of application "System Events" -- 归位
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				
				-- click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				
				delay 0.1
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				
				click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
				-- click button "成交" of window 1 of application process "同花顺" of application "System Events"
				-- click button "委托" of window 1 of application process "同花顺" of application "System Events"
				-- click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				
				-- 成交时间
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				
				if dateRange is "today" then
					click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisWeek" then
					click button "本周" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisMonth" then
					click button "本月" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisSeason" then
					click button "本季" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				else if dateRange is "thisYear" then
					click button "本年" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				delay 0.1
				
				-- return entire contents
				-- sometimes in area 4 sometimes in area 5					
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every text field of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every text field of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				
				try
					-- static text "警告" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- static text "业务提示:[]" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					-- button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", "警告"}
					end if
					return {"successed", comments, closedDeals}
				on error
					return {"successed", comments, closedDeals}
				end try
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getCapitalDetailsSim

on run {assetType, dateRange}
	-- assetType: "stock", "sciTech"
	-- dateRange: "today", "thisWeek", "thisMonth", "thisSeason", "thisYear"
	
	-- set assetType to "stock"
	-- set dateRange to "thisMonth"
	
	getCapitalDetailsSim(assetType, dateRange)
	
	-- ex
	-- osascript getCapitalDetailsSim.scpt stock thisSeason
end run
'"""

