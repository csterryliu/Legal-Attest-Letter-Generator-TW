require 'securerandom'

class WelcomeController < ApplicationController

	def index

	end

	def generate_pdf
		senderName = params[:senderName]
		senderAddr = params[:senderAddr]
		receiverName = params[:receiverName]
		receiverAddr = params[:receiverAddr]
		ccName = params[:ccName]
		ccAddr = params[:ccAddr]

		@name = SecureRandom.hex(13)
		@result = %x(cd python ; python3 tw-lal-generator.py test.txt --senderName #{senderName} --senderAddr #{senderAddr} --receiverName #{receiverName} --receiverAddr #{receiverAddr} --ccName #{ccName} --ccAddr #{ccAddr} --outputFileName ../public/download/#{@name}.pdf 2>&1)
		send_file( Rails.root.join('public/download', "#{@name}.pdf"), type: 'application/pdf')
	end

end
