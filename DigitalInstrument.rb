Shoes.app do
	keydown do |k|
		# Start playing piano key sounds here
		case k
		when 'a'
			para "you pressed a down\n"
		when 's'
			para "you pressed s down\n"
		end
		
		para "#{k.inspect} down\n"
	end
	keyup do |k|
		# Stop playing piano key sounds here
		case k
		when 'a'
			para "you pressed a up\n"
		when 's'
			para "you pressed s up\n"
		end
		
		para "#{k.inspect} up\n"
	end
end
