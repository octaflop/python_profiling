
# coding: utf-8

# # Python Profiling

# Profiling: Used to find bottlenecks in code

# ## Python

# `cProfile`

# In[24]:


import cProfile

import json

some_json = """
[
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}},
{"floors":[{"id":14,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"First Floor","description":""},{"id":15,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Mezzanine","description":null},{"id":11,"campus_id":12,"campus_name":"SweetCandy","building_id":12,"building_name":"SweetCandy","name":"Second Floor","description":""}],"meta":{"per_page":10,"total":3,"filtered_total":3,"page":1,"page_limit":100}}
]
"""

cProfile.run('json.loads(some_json)')


# In[25]:


# We can also save to a file and render an image
filename = 'json_loads'
cProfile.run('json.loads(some_json)', filename=f'{filename}.profile')


# In[26]:


import sh
# Convert the .profile -> .dot
sh.gprof2dot('-f', 'pstats', '-o', f'{filename}.dot', f'{filename}.profile')


# In[27]:


# Convert the .dot -> png
sh.dot('-T', 'png', f'{filename}.dot', '-o', f'{filename}.png')


# ![profiled image](./json_loads.png)

# ## More Python

# ### We only want to measure what we care about.

# In[28]:


import random
import sh

def setup_random_dict():
    raw = []
    for i in range(20):
        rand_foo = random.randint(1, 800)
        raw.append({
            'foo': f'bar_{rand_foo}',
            'id': random.randint(1, 800)
        })
    ret = json.dumps(raw)
    return ret


def generate_profile(filename):
    cProfile.run('setup_random_dict()', filename=f'{filename}.profile')
    # Convert the .profile -> .dot
    sh.gprof2dot('-f', 'pstats', '-o', f'{filename}.dot', f'{filename}.profile')
    # Convert the .dot -> png
    sh.dot('-T', 'png', f'{filename}.dot', '-o', f'{filename}.png')

# if __name__ == '__main__:'
generate_profile('random_thing')


# ![random_thing](./random_thing.png)

# ### Instead, we only decompose the function

# In[29]:


import random
import sh

def setup_random_dict():
    raw = []
    for i in range(20):
        rand_foo = random.randint(1, 800)
        raw.append({
            'foo': f'bar_{rand_foo}',
            'id': random.randint(1, 800)
        })
    return raw

raw = setup_random_dict()

def generate_profile(filename):
    cProfile.run('json.dumps(raw)', filename=f'{filename}.profile')
    # Convert the .profile -> .dot
    sh.gprof2dot('-f', 'pstats', '-o', f'{filename}.dot', f'{filename}.profile')
    # Convert the .dot -> png
    sh.dot('-T', 'png', f'{filename}.dot', '-o', f'{filename}.png')

# if __name__ == '__main__:'
generate_profile('just_json')


# ![just json](./just_json.png)

# ## Django
# ### 10x Easier
# https://pypi.org/project/yet-another-django-profiler/

# Add to middleware:

# In[30]:


# local_settings.py
MIDDLEWARE_CLASSES = () #...
MIDDLEWARE_CLASSES += ('yet_another_django_profiler.middleware.ProfilerMiddleware',)


# Now just add `?profile` to a URL!
# 
# https://ebdevi.io:8000/api/v4/deployment/filter/floors/11/rooms/?profile

# ![profile_example](https://user-images.githubusercontent.com/6115/40940549-63d07bf8-6805-11e8-9417-548e2110722b.png)

# ## Thanks
# 
# ### Special Thanks to: Jason
