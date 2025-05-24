from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'prescribemate.urls_main', name='www'),
    host(r'doctors', 'prescribemate.urls_doctors', name='doctors'),
    host(r'patients', 'prescribemate.urls_patients', name='patients'),
    host(r'hospitals', 'prescribemate.urls_hospitals', name='hospitals'),
    host(r'pharmacy', 'prescribemate.urls_pharmacy', name='pharmacy'),
)