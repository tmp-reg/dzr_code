-record(mail, {
		mail_id,
		sender_name,
		sender_id,
		mail_type,
		mail_title,
		mail_status = 1,
		timestamp,
		attachment_status = 2,
		goods_list = [],
		mail_content,
		silver_status,
		silver = 0,
		gold_status,
		gold = 0,
		bind_gold_status,
		bind_gold = 0,
		jungong_status,
		jungong = 0,
		goods_isbind = 0
			   }).