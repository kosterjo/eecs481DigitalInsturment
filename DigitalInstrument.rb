require 'shoes'

Shoes.app do
	@info = para "No key is pressed."
	keypress do |k|
		@info.replace "#{k} was pressed."
		debug(k)
	end
end