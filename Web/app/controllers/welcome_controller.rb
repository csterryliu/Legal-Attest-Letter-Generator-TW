require 'securerandom'

class WelcomeController < ApplicationController

	def index
		@name = SecureRandom.hex(13)
		@result = %x(cd $LALGPATH ; python3 tw-lal-generator.py test.txt --outputFileName Web/public/#{@name}.pdf 2>&1)
		@tt = "tttttt"
	end

end
