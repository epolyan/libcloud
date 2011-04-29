#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This example provides both a running script (invoke from command line)
# and an importable module one can play with in Interactive Mode.
#
# See docstrings for usage examples.
#
import sys
from pretty import pprint
import logging

from libcloud.common.base import ConnectionKey, LoggingHTTPConnection, LoggingHTTPSConnection

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

fh = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
logging.getLogger().addHandler(fh)
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def main(argv):
    """Main OpenStack Demo

    When invoked from the command line, it will connect using NOVA_API_KEY
    NOVA_USERNAME NOVA_URL environment variables, and perform the following
    tasks:

    - List current nodes
    - List available images (up to 10)
    - List available sizes (up to 10)
    - Create a single instance
    - Destroy it
    """



    OpenStackDriver = get_driver(Provider.OPENSTACK)

    import os
    try:
        open_stack = OpenStackDriver(key=os.environ['NOVA_USERNAME'], secret=os.environ['NOVA_API_KEY'], url=os.environ['NOVA_URL'])
        print ">> Loading nodes..."
        nodes = open_stack.list_nodes()
        pprint(nodes)
    except NameError, e:
        print ">> Fatal Error: %s" % e
        print "   (Hint: modify secrets.py.dist)"
        raise
    except Exception, e:
        print ">> Fatal error: %s" % e
        raise

    print ">> Loading images... (showing up to 10)"
    images = open_stack.list_images()
    pprint(images[:10])

    print ">> Loading sizes... (showing up to 10)"
    sizes = open_stack.list_sizes()
    pprint(sizes[:10])

    instance = open_stack.create_node(name='create_image_demo',
                           image=images[0],
                           size=sizes[0])
    instance.destroy()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

  
