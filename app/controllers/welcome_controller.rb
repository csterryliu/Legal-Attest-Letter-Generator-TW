require 'securerandom'

class WelcomeController < ApplicationController

	def index

	end

	def generate_pdf
		@name = SecureRandom.hex(13)
		@result = %x(cd python ; python3 tw-lal-generator.py test.txt --outputFileName ../public/download/#{@name}.pdf 2>&1)
		send_file( Rails.root.join('public/download', "#{@name}.pdf"), type: 'application/pdf')
	end

end
