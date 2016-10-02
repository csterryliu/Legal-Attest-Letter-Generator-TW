require 'securerandom'

class WelcomeController < ApplicationController

	def generate_pdf
		senderName = params[:senderName]
		senderAddr = params[:senderAddr]
		receiverName = params[:receiverName]
		receiverAddr = params[:receiverAddr]
		ccName = params[:ccName]
		ccAddr = params[:ccAddr]

		command = "python3 tw-lal-generator.py test.txt"
		
		if senderName != ''
			command << " --senderName #{senderName}"
		end
		if senderAddr != ''
			command << " --senderAddr #{senderAddr}"
		end
		if receiverName != ''
			command << " --receiverName #{receiverName}"
		end
		if receiverAddr != ''
			command << " --receiverAddr #{receiverAddr}"
		end
		if ccName != ''
			command << " --ccName #{ccName}"
		end
		if ccAddr != ''
			command << " --ccAddr #{ccAddr}"
		end

		@name = SecureRandom.hex(13)

		@result = %x(cd python ; #{command} --outputFileName ../public/download/#{@name}.pdf 2>&1)


		#@result = %x(cd python ; python3 tw-lal-generator.py test.txt --senderName #{senderName} --senderAddr #{senderAddr} --receiverName #{receiverName} --receiverAddr #{receiverAddr} --ccName #{ccName} --ccAddr #{ccAddr} --outputFileName ../public/download/#{@name}.pdf 2>&1)
		send_file( Rails.root.join('public/download', "#{@name}.pdf"), type: 'application/pdf')
	end

end
