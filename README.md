# eecs481DigitalInstrument

## Installation
Instructions to get "DigitalInstrumentWavAppender.rb" working:
This will take notes pressed and append them into a file called append.wav

First you need to install the `wavefile` gem. Run:

`gem install wavefile`

Next, in order to get it to work with the shoes GUI app, you have to copy the wavefile gem to the shoes directory with this command:

`cd ~ && cp -r .gem/ruby/gems/wavefile-0.7.0/ .shoes/walkabout/lib/ruby/gems/2.2.0/gems/`

or

`cd ~ && cp -r .rvm/gems/ruby-2.2.1/gems/wavefile-0.7.0/ .shoes/walkabout/lib/ruby/gems/2.2.0/gems/`

If you have a Ruby Version Manager installed on your machine (rvm).

Then you can run the shoes application and press open application. Select DigitalInstrumentWavAppender.rb

That should get you running

## Creating Music!!

Once you have this all installed, you can start creating music! Open up the shoes application, then from the shoes interface,select `Open an App`. From there, you can open the `DigitalInstrumentWavAppender.rb` to start creating music.

Once you have opened up the `DigitalInstrumentWavAppender.rb` application, you can press keys to append notes to a file, to be played back later. After you have finished pressing your keys, you can play these keys back, by opening up the `append.wav` file, and listening to the recorded music.
