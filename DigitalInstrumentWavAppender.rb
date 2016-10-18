require 'wavefile'
include WaveFile

# FILES_TO_APPEND = ["c1.wav", "e1.wav", "a1.wav"]
FILES_TO_APPEND = []
# files = []
SAMPLES_PER_BUFFER = 4096
stop = true

Shoes.app do
	keydown do |k|
		# Start playing piano key sounds here
		case k
		when 'a'
                        FILES_TO_APPEND.insert(-1, './notes/a1.wav')
		when 'b'
                        FILES_TO_APPEND.insert(-1, './notes/b1.wav')
		when 'c'
                        FILES_TO_APPEND.insert(-1, './notes/c1.wav')
                when 'q'
                        stop = true
                        break
                end

		para "#{k.inspect} down\n"
                break if stop
	end
        break if stop
end



Writer.new("append.wav", Format.new(:stereo, :pcm_16, 44100)) do |writer|
  FILES_TO_APPEND.each do |file_name|
    Reader.new(file_name).each_buffer(SAMPLES_PER_BUFFER) do |buffer|
      writer.write(buffer)
    end
  end
end
