require 'wavefile'
include WaveFile

FILES_TO_APPEND = []
SAMPLES_PER_BUFFER = 4096

def write_files(files)
    Writer.new("append.wav", Format.new(:stereo, :pcm_16, 44100)) do |writer|
        FILES_TO_APPEND.each do |file_name|
            Reader.new(file_name).each_buffer(SAMPLES_PER_BUFFER) do |buffer|
                writer.write(buffer)
            end
        end
    end
end

Shoes.app do
    para "Press 'a', 'b', or 'c' to write a note...\n"
    keydown do |k|
        # Start recording piano key sounds here
        case k
        when 'a'
            FILES_TO_APPEND.insert(-1, './notes/a1.wav')
            write_files(FILES_TO_APPEND)
        when 'b'
            FILES_TO_APPEND.insert(-1, './notes/b1.wav')
            write_files(FILES_TO_APPEND)
        when 'c'
            FILES_TO_APPEND.insert(-1, './notes/c1.wav')
            write_files(FILES_TO_APPEND)
        end
    para "#{k.inspect} down\n"
    end
end

