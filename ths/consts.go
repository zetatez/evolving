package ths

const AsIsClientLoggedIn = `osascript -e '
on isClientLoggedIn()
	tell application "System Events"
		tell application "System Events" to set isRunning to exists (processes where name is "同花顺")
		if isRunning then
			tell application "同花顺" to activate
			delay 4
			tell process "同花顺"
				delay 0.25
				set val to get value of attribute "AXTitle" of button of window 1 of application process "同花顺" of application "System Events"
				if val contains "游客登录" then
					return false
				end if
				return true
			end tell
		end if
	end tell
end isClientLoggedIn
isClientLoggedIn()
'`

const AsIsBrokerLoggedIn = `osascript -e '
on isBrokerLoggedIn()
	tell application "同花顺" to activate
	delay 0.8
	tell application "System Events"
		tell process "同花顺"
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			try
				set info to get value of attribute "AXTitle" of button of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				if info contains "退出" then
					return true
				end if
			on error
				return false
			end try
			return false
		end tell
	end tell
end isBrokerLoggedIn
isBrokerLoggedIn()
'`

const AsLoginClient = `osascript -e '
on loginClientHelp(userid, pwd)
	try
		tell application "同花顺" to quit
		delay 1
	end try
	tell application "同花顺" to activate
	delay 3
	tell application "System Events"
		tell process "同花顺"
			try
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to userid
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to pwd
				click button "登 录" of window 1 of application process "同花顺" of application "System Events"
				delay 10
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
	if isRunning then
		return "successed"
	else
		return "failed"
	end if
end loginClient

on run {userid, pwd}
	loginClient(userid, pwd)
end run
'`

const AsLogoutClient = `osascript -e '
on logoutClient()
	try
		tell application "同花顺" to quit
		return "successed"
	on error
		return "failed"
	end try
end logoutClient
logoutClient()
'`

const AsLoginBroker = `osascript -e '
on loginBroker(broker_name, trade_account, trade_pwd)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			try
				set info to get value of attribute "AXTitle" of button of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				if info contains "退出" then
					return "successed"
				end if
			on error
				try
					click button "立即登录" of window 1 of application process "同花顺" of application "System Events"
					click button 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set brokerName to broker_name
					set historyBrokers to get value of text field of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if historyBrokers is {} then
						return "failed"
					end if
					if historyBrokers contains brokerName then
						repeat with rowNum from 1 to length of historyBrokers
							set theCurrentListItem to item rowNum of historyBrokers
							if theCurrentListItem contains brokerName then
								exit repeat
							end if
						end repeat
					else
						return "failed"
					end if
					select text field rowNum of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set po to get position of text field rowNum of list 1 of scroll area 1 of combo box 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set po1 to get item 1 of po
					set po2 to get item 2 of po
					do shell script "/usr/local/bin/cliclick c:" & po1 & "," & po2
					delay 0.25
					set value of checkbox 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events" to trade_account
					set value of text field 1 of sheet 1 of window 1 of application process "同花顺" of application "System Events" to trade_pwd
					set verificationCodeList to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					set verificationCode to ""
					repeat with x from 8 to 12
						set verificationCode to verificationCode & item x of verificationCodeList
					end repeat
					set value of text field 2 of sheet 1 of window 1 of application process "同花顺" of application "System Events" to verificationCode
					click button "登录" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					try
						delay 2
						set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						set warningFlag to item 1 of info
						if warningFlag is "连接委托主站失败！可能是以下原因：" then
							click button "确定" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						end if
					end try
					return "successed"
				on error
					return "failed"
				end try
			end try
		end tell
	end tell
end loginBroker

on run {broker_name, trade_account, trade_pwd}
	loginBroker(broker_name, trade_account, trade_pwd)
end run
'`

const AsLogoutBroker = `osascript -e '
on logoutBroker()
	tell application "同花顺" to activate
	delay 0.25
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "退出" of UI element 2 of row 10 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				return "successed"
			on error
				return "failed"
			end try
		end tell
	end tell
end logoutBroker
logoutBroker()
'`

const AsTransferBank2Broker = `osascript -e '
on transfer(transferType, amount, bank_pwd, trade_pwd)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				click button "转账" of UI element 2 of row 9 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				set value of text field 1 of window "银证转账" of application process "同花顺" of application "System Events" to amount
				set value of text field 2 of window "银证转账" of application process "同花顺" of application "System Events" to bank_pwd
				set value of text field 3 of window "银证转账" of application process "同花顺" of application "System Events" to trade_pwd
				delay 0.1
				click button "确定转入券商" of window "银证转账" of application process "同花顺" of application "System Events"
				click button "确认" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
				delay 0.2
				try
					set info to get value of static text of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
						click button 6 of window "银证转账" of application process "同花顺" of application "System Events"
						return {"failed", "警告:外部机构[5200]不支持7*24银证业务"}
					end if
				end try
				try
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
	transfer(transferType, amount, bank_pwd, trade_pwd)
end run
'`

const AsTransferBroker2Bank = `osascript -e '
on transfer(transferType, amount, bank_pwd, trade_pwd)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				click button "转账" of UI element 2 of row 9 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
				delay 0.25
				click button 2 of window "银证转账" of application process "同花顺" of application "System Events"
				set value of text field 1 of window "银证转账" of application process "同花顺" of application "System Events" to amount
				set value of text field 2 of window "银证转账" of application process "同花顺" of application "System Events" to bank_pwd
				set value of text field 3 of window "银证转账" of application process "同花顺" of application "System Events" to trade_pwd
				delay 0.1
				click button "确定转入银行" of window "银证转账" of application process "同花顺" of application "System Events"
				click button "确认" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
				delay 0.2
				try
					set info to get value of static text of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
					if info contains "警告" then
						click button "确认" of sheet 1 of window "银证转账" of application process "同花顺" of application "System Events"
						click button 6 of window "银证转账" of application process "同花顺" of application "System Events"
						return {"failed", "警告:外部机构[5200]不支持7*24银证业务"}
					end if
				end try
				try
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
	transfer(transferType, amount, bank_pwd, trade_pwd)
end run
'`

const AsRevokeAllEntrust = `osascript -e '
on revokeAllEntrust()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				return {"successed"}
			on error
				return {"failed"}
			end try
		end tell
	end tell
end revokeAllEntrust
revokeAllEntrust()
'`

const AsOneKeyIPO = `osascript -e '
on oneKeyIPO()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "新股申购" of window 1 of application process "同花顺" of application "System Events"
				delay 1
				click button "一键申购" of window 1 of application process "同花顺" of application "System Events"
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
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
'`

const AsGetAccountInfo = `osascript -e '
on getAccountInfo()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
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
'`

const AsGetHoldingSharesStock = `osascript -e '
on getHoldingShares(assetType)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
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
	getHoldingShares(assetType)
end run
'`

const AsGetHoldingSharesSciTech = `osascript -e '
on getHoldingShares(assetType)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
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
	getHoldingShares(assetType)
end run
'`

const AsGetHoldingSharesGem = `osascript -e '
on getHoldingShares(assetType)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
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
	getHoldingShares(assetType)
end run
'`

const AsIssuingEntrustBuyStock = `osascript -e '
on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
					if price is "- -" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				click button "确定买入" of window 1 of application process "同花顺" of application "System Events"
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
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"警告"} then
					set flag to -1
				end if
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				delay 0.6
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set contractNoList to {}
				set contractNoList1 to {}
				set contractNoList2 to {}
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
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsIssuingEntrustSellStock = `osascript -e '
on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
					if price is "- -" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				click button "确定卖出" of window 1 of application process "同花顺" of application "System Events"
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
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"警告"} then
					set flag to -1
				end if
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				delay 0.6
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set contractNoList to {}
				set contractNoList1 to {}
				set contractNoList2 to {}
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
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsIssuingEntrustBuySciTech = `osascript -e '
on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
					if price is "- -" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				click button "确定买入" of window 1 of application process "同花顺" of application "System Events"
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
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"警告"} then
					set flag to -1
				end if
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				delay 0.6
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set contractNoList to {}
				set contractNoList1 to {}
				set contractNoList2 to {}
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
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsIssuingEntrustSellSciTech = `osascript -e '
on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
					if price is "- -" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				click button "确定卖出" of window 1 of application process "同花顺" of application "System Events"
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
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"警告"} then
					set flag to -1
				end if
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				delay 0.6
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set contractNoList to {}
				set contractNoList1 to {}
				set contractNoList2 to {}
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
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsIssuingEntrustBuyGem = `osascript -e '
on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
					if price is "- -" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				click button "确定买入" of window 1 of application process "同花顺" of application "System Events"
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
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"警告"} then
					set flag to -1
				end if
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				delay 0.6
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set contractNoList to {}
				set contractNoList1 to {}
				set contractNoList2 to {}
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
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsIssuingEntrustSellGem = `osascript -e '
on issuingEntrust(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				click button "买入" of window 1 of application process "同花顺" of application "System Events"
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
					if price is "- -" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				click button "确定卖出" of window 1 of application process "同花顺" of application "System Events"
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
					delay 0.01
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end if
				set flag to 0
				set info to ""
				try
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				if info contains {"警告"} then
					set flag to -1
				end if
				delay 0.1
				if flag is not 0 then
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"failed", flag, info}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if checkboxStatus is true then click theCheckbox
				end tell
				delay 0.6
				try
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment2 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments2 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set contractNoList to {}
				set contractNoList1 to {}
				set contractNoList2 to {}
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
	issuingEntrust(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsGetEntrustToday = `osascript -e '
on getEntrust(assetType, dateRange, isRevocable)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.01
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				delay 0.1
				set theCheckbox to checkbox 1 of window 1 of application process "同花顺" of application "System Events"
				tell theCheckbox
					set checkboxStatus to value of theCheckbox as boolean
					if isRevocable is "true" then
						if checkboxStatus is false then click theCheckbox
					else
						if checkboxStatus is true then click theCheckbox
					end if
				end tell
				try
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				try
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
	getEntrust(assetType, dateRange, isRevocable)
end run
'`

const AsGetClosedDealsToday = `osascript -e '
on getClosedDeals(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				end if
				click button "成交" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of pop over 1 of window 1 of application process "同花顺" of application "System Events"
				delay 0.45
				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				try
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
	getClosedDeals(assetType, dateRange)
end run
'`

const AsGetBidsStock = `osascript -e '
on getBids(assetType, stockCode)
	tell application "同花顺" to activate
	delay 0.25
	tell application "System Events"
		tell process "同花顺"
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			click button "股票" of window 1 of application process "同花顺" of application "System Events"
			try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
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
	getBids(assetType, stockCode)
end run
'`

const AsGetBidsSciTech = `osascript -e '
on getBids(assetType, stockCode)
	tell application "同花顺" to activate
	delay 0.25
	tell application "System Events"
		tell process "同花顺"
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
			try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
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
	getBids(assetType, stockCode)
end run
'`

const AsGetBidsGem = `osascript -e '
on getBids(assetType, stockCode)
	tell application "同花顺" to activate
	delay 0.25
	tell application "System Events"
		tell process "同花顺"
			click button 6 of window 1 of application process "同花顺" of application "System Events"
			click button "模拟" of window 1 of application process "同花顺" of application "System Events"
			click button "A股" of window 1 of application process "同花顺" of application "System Events"
			click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
			try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				click button "卖出" of window 1 of application process "同花顺" of application "System Events"
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
	getBids(assetType, stockCode)
end run
'`

const AsRevokeEntrustAllBuyAndSellStock = `osascript -e '
on revokeEntrust(revokeType, assetType, contractNo)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.2
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", "revoke allBuyAndSell stock is successed"}
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
	revokeEntrust(revokeType, assetType, contractNo)
end run
'`

const AsRevokeEntrustAllBuyAndSellSciTech = `osascript -e '
on revokeEntrust(revokeType, assetType, contractNo)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.2
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", "revoke allBuyAndSell sciTech is successed"}
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
	revokeEntrust(revokeType, assetType, contractNo)
end run
'`

const AsRevokeEntrustAllBuyAndSellGem = `osascript -e '
on revokeEntrust(revokeType, assetType, contractNo)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.2
				click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", "revoke allBuyAndSell gem is successed"}
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
	revokeEntrust(revokeType, assetType, contractNo)
end run
'`

const AsGetTodayIPO = `osascript -e '
on getTodayIPO()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "新股申购" of window 1 of application process "同花顺" of application "System Events"
				delay 1.2
				set comment to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events"
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
'`

const AsGetTransferRecords = `osascript -e '
on getTransferRecords(dateRange)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
				click button "流水" of UI element 2 of row 9 of table 1 of scroll area 1 of window 1 of application process "同花顺" of application "System Events"
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
				click button 1 of window "查询流水" of application process "同花顺" of application "System Events"
				return {"successed", comment, info}
			on error
				return {"failed", "unknown err"}
			end try
		end tell
	end tell
end getTransferRecords

on run {dateRange}
	getTransferRecords(dateRange)
end run
'`

const AsRevokeAllBuyEntrust = `osascript -e '
on revokeAllBuyEntrust()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"

				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try

				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try

				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				return "successed"
			on error
				return "failed"
			end try
		end tell
	end tell
end revokeAllBuyEntrust

revokeAllBuyEntrust()
'`

const AsRevokeAllSellEntrust = `osascript -e '
on revokeAllSellEntrust()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"

				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try

				click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try

				click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.08
				click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
				end try
				return "successed"
			on error
				return "failed"
			end try
		end tell
	end tell
end revokeAllSellEntrust

revokeAllSellEntrust()
'`

const AsGetCapitalDetails = `osascript -e '
on getCapitalDetails(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"

				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "sciTech" then
					click button "科创板盘后" of window 1 of application process "同花顺" of application "System Events"
				else if assetType is "gem" then
					click button "创业板盘后" of window 1 of application process "同花顺" of application "System Events"
				end if

				click button "资金明细" of window 1 of application process "同花顺" of application "System Events"
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

				try
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every text field of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every text field of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try

				try
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
	getCapitalDetails(assetType, dateRange)
end run
'`

const AsGetIPO = `osascript -e '
on getIPO(queryType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"

				click button "新股申购" of window 1 of application process "同花顺" of application "System Events"

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
	getIPO(queryType, dateRange)
end run
'`
