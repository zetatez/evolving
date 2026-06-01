package ths

const AsGetAccountInfoSim = `osascript -e '
on getAccountInfoSim()
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "A股" of window 1 of application process "同花顺" of application "System Events"
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
'`

const AsIssuingEntrustSim = `osascript -e '
on issuingEntrustSim(tradingAction, assetType, stockCode, price, amount)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
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
				try
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set revocableEntrustment1 to get value of static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set comments1 to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if tradingAction is "buy" then
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
					click button "买入" of window 1 of application process "同花顺" of application "System Events"
				else if tradingAction is "sell" then
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
					click button "买入" of window 1 of application process "同花顺" of application "System Events"
					click button "卖出" of window 1 of application process "同花顺" of application "System Events"
				end if
				set value of attribute "AXFocused" of text field 2 of window 1 of application process "同花顺" of application "System Events" to true
				set value of text field 2 of window 1 of application process "同花顺" of application "System Events" to stockCode
				if price is "None" then
					delay 0.05
					if tradingAction is "buy" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
						if price is "- -" then
							set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 1 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
						end if
					else if tradingAction is "sell" then
						set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 3 of window 1 of application process "同花顺" of application "System Events")
						if price is "- -" then
							set price to item 1 of item 1 of (get value of attribute "AXTitle" of every button of every UI element of row 5 of table 1 of scroll area 2 of window 1 of application process "同花顺" of application "System Events")
						end if
					end if
				end if
				delay 0.25
				set value of text field 1 of window 1 of application process "同花顺" of application "System Events" to price
				set value of text field 3 of window 1 of application process "同花顺" of application "System Events" to amount
				if tradingAction is "buy" then
					click button "确定买入" of window 1 of application process "同花顺" of application "System Events"
				else if tradingAction is "sell" then
					click button "确定卖出" of window 1 of application process "同花顺" of application "System Events"
				end if
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
				delay 0.25
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
end issuingEntrustSim

on run {tradingAction, assetType, stockCode, price, amount}
	issuingEntrustSim(tradingAction, assetType, stockCode, price, amount)
end run
'`

const AsGetHoldingSharesSim = `osascript -e '
on getHoldingSharesSim(assetType)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option: " & assetType}
				end if
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
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
	getHoldingSharesSim(assetType)
end run
'`

const AsGetEntrustSim = `osascript -e '
on getEntrustSim(assetType, dateRange, isRevocable)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "持仓" of window 1 of application process "同花顺" of application "System Events"
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				click button "今天" of window 1 of application process "同花顺" of application "System Events"
				delay 0.1
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
					set info to get value of static text of sheet 1 of window 1 of application process "同花顺" of application "System Events"
					if info is {"警告", "不支持历史委托查询"} then
						click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
						return {"failed", info}
					end if
				end try
				try
					set revocableEntrustment to get value of static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
					return {"successed", comments, revocableEntrustment}
				on error
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
	getEntrustSim(assetType, dateRange, isRevocable)
end run
'`

const AsRevokeEntrustSim = `osascript -e '
on revokeEntrustSim(revokeType, assetType, contractNo)
	tell application "同花顺" to activate
	delay 0.4
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				if assetType is "stock" then
					click button "股票" of window 1 of application process "同花顺" of application "System Events"
				else
					return {"failed", "wrong option"}
				end if
				click button "委托" of window 1 of application process "同花顺" of application "System Events"
				delay 0.2
				if revokeType is "allBuyAndSell" then
					click button "全撤" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "allBuy" then
					click button "撤买" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "allSell" then
					click button "撤卖" of window 1 of application process "同花顺" of application "System Events"
				else if revokeType is "contractNo" then
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
							return {"successed", "contract No. " & contractNo & " was not found"}
						end if
					end if
					if idarea is 4 then
						set po to get position of (get item 11 of (get static text of row rowNum of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"))
					else if idarea is 5 then
						set po to get position of (get item 11 of (get static text of row rowNum of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"))
					end if
					set po1 to get item 1 of po
					set po2 to get item 2 of po
					do shell script "/usr/local/bin/cliclick dc:" & po1 & "," & po2
				end if
				try
					click button "确认" of sheet 1 of window 1 of application process "同花顺" of application "System Events"
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
	revokeEntrustSim(revokeType, assetType, contractNo)
end run
'`

const AsGetClosedDealsSim = `osascript -e '
on getClosedDealsSim(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
				click button "成交" of window 1 of application process "同花顺" of application "System Events"
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
					set closedDeals to get value of every static text of every row of table 1 of scroll area 4 of window 1 of application process "同花顺" of application "System Events"
				on error
					set comments to get value of attribute "AXTitle" of button of group 1 of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
					set closedDeals to get value of every static text of every row of table 1 of scroll area 5 of window 1 of application process "同花顺" of application "System Events"
				end try
				try
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
	getClosedDealsSim(assetType, dateRange)
end run
'`

const AsGetCapitalDetailsSim = `osascript -e '
on getCapitalDetailsSim(assetType, dateRange)
	tell application "同花顺" to activate
	delay 0.5
	tell application "System Events"
		tell process "同花顺"
			try
				click button 1 of window 1 of application process "同花顺" of application "System Events"
				click button 6 of window 1 of application process "同花顺" of application "System Events"
				click button "模拟" of window 1 of application process "同花顺" of application "System Events"
				delay 0.1
				click button "股票" of window 1 of application process "同花顺" of application "System Events"
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
	getCapitalDetailsSim(assetType, dateRange)
end run
'`
