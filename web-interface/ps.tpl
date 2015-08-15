%for line in iter(process.stdout.readline, ''):
    %line = line.strip()
{{line}}<br/>
%end
