#     Copyright 2014 Asurion.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import argparse
from setup_infra import scheduler_sleep


def validate_int_arg(arg):
    strvalue = str(arg)
    intvalue = int(arg)
    if len(strvalue) != 12:
        raise argparse.ArgumentTypeError('%r Length of an account number must 12, given {}'.format(len(strvalue)) % strvalue)
    if not int(intvalue):
        raise argparse.ArgumentTypeError('%r must be an integer' % intvalue)
    return arg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='AWS EC2 Scheduler:Sleep',
                                     description= 'Multi account ec2 sleep utility for businesses operating multiple accounts.',
                                     usage='%(prog)s [options]')

    parser.add_argument('--profile',
                        required=True,
                        help='lambda function will live in this account.')
    parser.add_argument('--region',
                        required=True,
                        help='lambda function will live in this region.')
    parser.add_argument('--rootnode',
                        type=validate_int_arg,
                        required=True,
                        help='account number, for the -p profile argument.')

    parser.add_argument('--leafnode',
                        type=validate_int_arg,
                        required=True,
                        help='account number, you want the lambda function to describe and validate tags here.')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    scheduler_sleep(vars(args))












