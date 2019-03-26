###############################################################################
#
#   Copyright 2019 Secretaría de Estado para el Avance Digital (SEAD)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#                     MEDDOCAN Format Converter Script
#
# This script is distributed as apart of the Medical Document Anonymization
# (MEDDOCAN) task. It is intended to be used via command line:
#
# $> python converter.py -i input_folder/ -o output_folder/
#
# It converts files between MEDDOCAN-Brat, MEDDOCAN-XML, and i2b2 formats.
# The mapping between the different formats is defined in the files in the
# mappings/ folders. See README file for further information.
#
# Input and target directories, as well as source and target formats can be
# chosen via command line.

import os
import argparse
import time
import csv
from lxml import etree
from lxml.etree import CDATA


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        os.makedirs(prospective_dir)
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


class Brat_format(object):

    def __init__(self, input_dir, output_dir, file_name):
        self.id = file_name
        self.in_file = os.path.join(input_dir, self.id) + '.txt'
        self.ann_file = os.path.join(input_dir, self.id) + '.ann'
        self.out_xml_file = os.path.join(output_dir, self.id) + '.xml'
        self.text = None
        self.annotations = []

    def load_annotations(self):

        try:
            text_file = open(self.in_file, "r")
            self.text = text_file.read()
            text_file.close()

        except IOError:
            if not args.quiet:
                print("File '" + self.in_file + "' does not exist!")

        try:
            ann_file = open(self.ann_file, 'r')
            for row in ann_file:
                line = row.strip()
                if line.startswith("T"):  # Lines is a Brat TAG
                    try:
                        annotation_id = line.split("\t")[0]
                        label = line.split("\t")[1].split()
                        tag = label[0]
                        start = int(label[1])
                        end = int(label[2])
                        form = line.split("\t")[2]

                        self.annotations.append({'id': annotation_id,
                                                 'start': start,
                                                 'end': end,
                                                 'text': form,
                                                 'TYPE': tag,
                                                 'comment': ''})

                    except IndexError:
                        if not args.quiet:
                            print("ERROR1! Index error while splitting sentence '" + line
                                  + "' in document '" + ann_file + "'!")
                if line.startswith("#"): # Line is a Brat comment
                    if args.verbose:
                        print("\tSkipping line (comment):\t" + line)
                    try:
                        label = line.split("\t")[1].split()
                        annotation_id = label[1]
                        comment = line.split("\t")[2]

                        for ann in self.annotations:
                            for key, value in ann.items():
                                if ann[key] == annotation_id:
                                    ann.update({'comment': comment})
                                    print("Updated " + annotation_id + " with comment '" + comment + "'.")

                    except IndexError:
                        if not args.quiet:
                            print("ERROR! Index error while splitting sentence '" + line
                                  + "' in document '" + ann_file + "'!")
            ann_file.close()
        except IOError:
            if not args.quixmlet:
                print("Error while reading '" + self.in_file + "'!")

    def write_to_xml(self, source_format, target_format):

        map_category = dict(csv.reader(open('mappings/' +
                                            source_format + '_to_' +
                                            target_format + '_map_categories.csv')))
        map_types = dict(csv.reader(open('mappings/' +
                                         source_format + '_to_' +
                                         target_format + '_map_types.csv')))

        root = etree.Element(map_category['ROOT'])

        text = etree.SubElement(root, 'TEXT')
        text.text = CDATA(self.text)

        tags = etree.SubElement(root, 'TAGS')

        for ann in sorted(self.annotations, key=lambda k: int(k['start'])):
            annotation = etree.SubElement(tags, map_category[ann['TYPE']])
            annotation.set('id', ann['id'])
            annotation.set('start', str(ann['start']))
            annotation.set('end', str(ann['end']))
            annotation.set('text', ann['text'])
            annotation.set('TYPE', map_types[ann['TYPE']])
            annotation.set('comment', ann['comment'])

        out = etree.tostring(root, pretty_print=True, xml_declaration='True', encoding='UTF-8')

        with open(self.out_xml_file, 'w', encoding='UTF-8') as f:
            f.write(out.decode())


class i2b2_format(Brat_format):

    def __init__(self, input_dir, output_dir, file_name):
        self.id = file_name
        self.in_file = os.path.join(input_dir, self.id) + '.xml'
        self.ann_file = os.path.join(output_dir, self.id) + '.ann'
        self.out_txt_file = os.path.join(output_dir, self.id) + '.txt'
        self.out_xml_file = os.path.join(output_dir, self.id) + '.xml'
        self.content = None
        self.text = None
        self.root = None
        self.annotations = []

    def load_annotations(self):

        try:
            if self.id is not None:
                self.content = open(self.in_file, 'r').read()

                tree = etree.parse(self.in_file)
                root = tree.getroot()

                self.root = root.tag

                try:
                    self.text = root.find("TEXT").text
                except AttributeError:
                    self.text = None

                for annotation in root.find("TAGS"):
                    self.annotations.append({'id': annotation.get('id'),
                                             'start': annotation.get('start'),
                                             'end': annotation.get('end'),
                                             'text': annotation.get('text'),
                                             'TYPE': annotation.get('TYPE'),
                                             'comment': annotation.get('comment')})
        except IOError:
            if not args.quiet:
                print("File '" + self.in_file + "' does not exist!")

    def write_to_brat(self, source_format):
        map_types = dict(csv.reader(open('mappings/' +
                                         source_format +
                                         '_to_brat_map_types.csv')))

        with open(self.out_txt_file, 'w', encoding='UTF-8') as f:
            f.write(self.text)

        with open(self.ann_file, 'w', encoding='UTF-8') as f:
            for ann in sorted(self.annotations, key=lambda k: int(k['start'])):
                tag = ann['id'] + "\t" + \
                      map_types[ann['TYPE']] + " " + \
                      ann['start'] + " " + \
                      ann['end'] + "\t" + \
                      ann['text'] + "\n"
                f.write(tag)


def process_corpus(corpus_list, input_dir, output_dir, source_format, target_format):
    if not args.quiet:
        print ("Processing corpus...\n")

    for filename in corpus_list:
        if args.verbose:
            print ("\tProcessing '" + filename + "'...")

        if source_format == "brat":
            brat_file = Brat_format(input_dir, output_dir, filename)
            brat_file.load_annotations()
            brat_file.write_to_xml(source_format, target_format)
        else:
            xml_file = i2b2_format(input_dir, output_dir, filename)
            xml_file.load_annotations()
            if target_format == "brat":
                xml_file.write_to_brat(source_format)
            else:
                xml_file.write_to_xml(source_format, target_format)

    if not args.quiet:
        print("\nCorpus processing completed!\n")


def load_corpus(input_dir):
    if not args.quiet:
        print ("Loading list of files...")
    corpus = []
    for subdir, dirs, files in os.walk(input_dir):
        for text_filename in files:
            corpus.append(os.path.splitext(text_filename)[0])
    if not args.quiet:
        print ("Corpus file list loaded!\n")
    return corpus


if __name__ == '__main__':

    start_time = time.time()

    # Read command line parameters
    parser = argparse.ArgumentParser(description="Script to convert between MEDDOCAN-BRAT/MEDDOCAN-XML/i2b2 formats.")

    parser.add_argument('-i', '--input_dir',
                        type=readable_dir,
                        help="Folder with the original input files",
                        default='input')
    parser.add_argument('-o', '--output_dir',
                        type=readable_dir,
                        help="Folder to store the output converted files",
                        default='output')
    parser.add_argument('-s', '--source',
                        choices=['brat', 'xml', 'i2b2'],
                        help="Format of source files",
                        default='brat')
    parser.add_argument('-t', '--target',
                        choices=['brat', 'xml', 'i2b2'],
                        help="Format of target files",
                        default='xml')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-v', '--verbose',
                       help="Increase output verbosity",
                       action='store_true')
    group.add_argument('-q', '--quiet',
                       help="Do not print anything",
                       action='store_true')

    args = parser.parse_args()

    if args.source == args.target:
        print("\nWARNING: Can't convert from '" +
              args.source + "' to '" + args.target +
              "' (same format). Save CPU. Save energy. Be green.\n")
    else:
        if not args.quiet:
            print("Converting your corpus...\n")
        my_corpus_list = load_corpus(args.input_dir)
        process_corpus(my_corpus_list, args.input_dir, args.output_dir, args.source, args.target)
        if not args.quiet:
            print("Processing time: %.2f seconds.\n" % (time.time() - start_time))
