class WelcomeController < ApplicationController

	def index
		@result = %x(cd $LALGPATH ; python3 $LALGPATH/tw-lal-generator.py $LALGPATH/test.txt 2>&1)
		@tt = "tttttt"
	end

end
