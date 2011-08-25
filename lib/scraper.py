import urllib2

hci_base = "http://www.hcii.cmu.edu/"
faculty_page = "people/faculty"
affiliated_page = "people/affiliated-faculty"
phd_page = "people/phd"
masters_page = "people/mhci"
undergrad_page = "people/bhci"
admin_staff_page = "people/administrative-staff"
tech_staff_page = "people/technical-staff"


def getPage(url):
	handler = urllib2.urlopen(url)
	lines = handler.readlines()
	handler.close()
	return lines

def getPeople(lines):
	counter = 0
	people = [ ]
	person = ""
	reading = False
	for line in lines:
		if "<table class=\"bio\"" in line:
			counter+=1
			reading = True
			person += line
		elif "</table>" in line:
			person += line
			people.append(person)
			person = ""
			reading = False
		elif reading:
			person += line
	# Get rid of the last table closer
	people = people[:len(people)-1]
	return people

def parsePerson(person):
	data = { }
	# Get the photo, which is separate from everything else
	photoTag = "<td class=\"photo\">"
	detailsTag = "<td class=\"details\">"
	detailsStart = 0
	try:
		startIndex = person.index(photoTag)
		endIndex = person.index("</td>", startIndex)
		detailsStart = endIndex + len("</td>")
		photoString = person[startIndex:endIndex+len("</td>")]
		imageStart = photoString.index("<img src=\"") +\
					       len("<img src=\"")
		imageEnd = photoString.index("\"", imageStart) - 1
		data["image"] = photoString[imageStart:imageEnd+1]
	except Exception as e:
		pass
		#print "No image found"
	
	# Now get the rest of the details
	while person.find("<div", detailsStart) != -1:
		divStart = person.index("<div", detailsStart)
		divEnd = person.index("</div>", divStart) + len("</div>")
		details = person[divStart:divEnd]
		detailsStart = divEnd
		tagEnd = details.index(">")+1
		divTag = details[:tagEnd]
		try:
			classStart = divTag.index("\"")
			classEnd = divTag.index("\"", classStart + 1)
			klass = divTag[(classStart+1):classEnd]
			if klass ==\
			"field field-type-text field-field-node-title":
				start = details.index(">", tagEnd) + 1
				end = details.index("<", start)
				names = details[start:end].strip().split(" ")
				if len(names) == 1:
					print "Name is " + names[0] + "?"
					data["first_name"] = names[0]
					data["last_name"] = ""
				elif len(names) == 2:
					data["first_name"] = names[0]
					data["last_name"] = names[1]
				else:
					data["first_name"] = names[0]
					data["last_name"] = names[-1]
			elif klass ==\
			"field field-type-text field-field-title":
				start = tagEnd
				end = details.index("<", tagEnd)
				value = details[start:end].strip()
				if len(value) > 0:
					data["title"] = value
			elif klass ==\
			"field field-type-text field-field-office":
				start = tagEnd
				end = details.index("<", tagEnd)
				value = details[start:end].strip()
				if len(value) > 0:
					data["room"] = value
			elif klass ==\
			"field field-type-text field-field-department":
				start = tagEnd
				end = details.index("<", tagEnd)
				value = details[start:end].strip()
				if len(value) > 0:
					data["department"] = value
			elif klass ==\
			"field field-type-link field-field-webpage":
				subDetails =\
					details[tagEnd:details.index("</div")]
				if len(subDetails.strip()) == 0: break
				start = subDetails.index(">") + 1
				end = subDetails.index("<", start)
				value = subDetails[start:end].strip()
				if value == "WWW":
					start = subDetails.index("\"") + 1
					end = subDetails.index("\"", start)
					value = subDetails[start:end].strip()
				if len(value) > 0:
					data["website"] = value
			elif klass ==\
			"field field-type-ca-phone field-field-phone":
				start = tagEnd
				end = details.index("<", tagEnd)
				value = details[start:end].strip()
				if len(value) > 0:
					data["phone"] = value
			elif klass ==\
			"field field-type-text " +\
			"field-field-department-unrestricted":
				start = tagEnd
				end = details.index("<", tagEnd)
				value = details[start:end].strip()
				if len(value) > 0:
					data["department_unrestricted"] = value
			elif klass ==\
			"field field-type-text field-field-email-plaintext":
				start = tagEnd
				end = details.index("<", tagEnd)
				value = details[start:end].strip()
				if len(value) > 0:
					data["email"] = value
			elif klass ==\
			"field field-type-text " +\
			"field-field-administrative-staff":
				start = tagEnd
				end = len(details)-len("</div>")
				value = details[start:end].strip()
				if len(value) > 0:
					data["admin"] = value
			elif klass == "field-label":
				start = divEnd
				end = person.index("</td>", detailsStart)
				value = person[start:end].strip()
				if len(value) > 0:
					data["concentrations"] = value
			elif klass ==\
			"field field-type-text field-field-nationality":
				start = divEnd
				end = details.index("</div>")
				value = details[start:end].strip()
				if len(value) > 0:
					data["nationality"] = value
			elif klass ==\
			"field field-type-text field-field-mhci-program":
				start = details.index(">", divEnd) + 1
				end = details.index("<", start)
				value = details[start:end].strip()
				if len(value) > 0:
					data["mhci_program"] = value
			elif klass ==\
			"field field-type-text field-field-mhci-project":
				start = details.index(">", divEnd) + 1
				end = details.index("<", start)
				value = details[start:end].strip()
				if len(value) > 0:
					data["mhci_project"] = value
			else:
				print "Have not implemented scrape for " +\
					klass + " yet"
		except Exception:
			data["concentrations"] =\
			details[divEnd:details.index("</div>")].strip()
	return data

keys = ["level", "first_name", "last_name", "title", "office", "image"]

def makeHash(url, level, output):
	file = open(output, "a")
	page = getPage(url)
	people = getPeople(page)
	for person in people:
		data = parsePerson(person)
		data["level"] = level
		if len(data.keys()) == 1:
			print "huh"
		else:
			s = "{"
			for key in data:
				if key in keys:
					s += "\"" + key + "\"=>\"" +\
						data[key] + "\", "
			s = s[:-2]
			s += "},\n"
			file.write(s)
	file.close()

def runAll():
	makeHash(hci_base + faculty_page, "faculty", "info.txt")
	makeHash(hci_base + affiliated_page, "affiliated", "info.txt")
	makeHash(hci_base + phd_page, "phd", "info.txt")
	makeHash(hci_base + masters_page, "masters", "info.txt")
	makeHash(hci_base + admin_staff_page, "staff", "info.txt")
	makeHash(hci_base + tech_staff_page, "staff", "info.txt")
	
