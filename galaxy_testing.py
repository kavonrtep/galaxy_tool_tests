#!/usr/bin/env python3
import time
import argparse
from collections import OrderedDict
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.tools.inputs import inputs, dataset, conditional
from tests import tools, files_to_upload

def make_inputs(input_params):
    ''' input builder'''
    tool_inputs = inputs()
    for i in input_params:
        tool_inputs = tool_inputs.set(i, input_params[i])
    return tool_inputs


def add_files_to_new_history(gi, files, history_name = "new history"):
    ''' upload file and retust datasets id in dictionary'''
    history = gi.histories.create_history(history_name)
    # files upload:
    dataset_id = {}
    for f in files:
        dataset_id[f] = gi.tools.upload_file(files[f], history['id'])['outputs'][0]['id']
    return dataset_id, history

def create_run_definition(dataset_id, tool_dict):
    '''define jobs for galaxy'''
    filtering_runs=[
        {'tool' : tool_dict['paired_fastq_filtering'],
         'inputs' : OrderedDict([
             ('A', dataset(dataset_id['fq1'])),
             ('B', dataset(dataset_id['fq2']))
         ])
        },
        {'tool' : tool_dict['paired_fastq_filtering'],
         'inputs' : OrderedDict([
             ('A', dataset(dataset_id['fq1'])),
             ('B', dataset(dataset_id['fq2'])),
             ('sampling', conditional().set('sequence_sampling', 'true').set('sample_size', 500))
         ])
        },
        {'tool' : tool_dict['single_fastq_filtering'],
         'inputs' : OrderedDict([
             ('A', dataset(dataset_id['fq1'])),
             ('sampling', conditional().set('sequence_sampling', 'true').set('sample_size', 500))
         ])
        }

    ]
    affixer_runs=[
        {'tool' : tool_dict['fasta_affixer'],
         'inputs' : OrderedDict([
             ('input', dataset(dataset_id['input_fasta'])),
             ('prefix', "PREFIX"),
             ('suffix', 'SUFFIX')
         ])
        },
        {'tool' : tool_dict['names_affixer'],
         'inputs' : OrderedDict([
             ('input', dataset(dataset_id['fq1'])),
             ('prefix', "PREFIX"),
             ('suffix', 'SUFFIX')
         ])
        }
    ]
    various_utils = [
        {'tool' : tool_dict['sampler'],
         'inputs' : OrderedDict([
             ('input', dataset(dataset_id['input_fasta'])),
             ('number', 500)
         ])
        },
        {'tool' : tool_dict['fasta_interlacer'],
         'inputs' : OrderedDict([
             ('A', dataset(dataset_id['fastaA'])),
             ('B', dataset(dataset_id['fastaB']))
         ])
        },
        {'tool' : tool_dict['rename_sequences'],
         'inputs' : OrderedDict([
             ('input', dataset(dataset_id['fastaA'])),
             ('prefix_length', 3)
         ])
        },
        {'tool' : tool_dict['chip_seq_ratio'],
         'inputs' : OrderedDict([
             ('ChipSeq', dataset(dataset_id['chip_fasta'])),
             ('InputSeq', dataset(dataset_id['input_fasta'])),
             ('Contigs', dataset(dataset_id['clustering_contigs']))
         ])
        },
        {'tool' : tool_dict['pair_scan'],
         'inputs' : OrderedDict([
             ('fasta_input', dataset(dataset_id['interlaced_fasta']))
         ])
        }

    ]

    dante_runs = [
        {'tool' : tool_dict['dante'],
         'inputs' : OrderedDict([
             ('input_type', conditional().set(
                 'input_type_selector', 'fasta').set(
                     'input_sequences', dataset(dataset_id['gepy_genome'])
                 )
             )
         ])
        },
        {'tool' : tool_dict['dante'],
         'inputs' : OrderedDict([
             ('input_type', conditional().set(
                 'input_type_selector', 'aln').set(
                     'input_sequences', dataset(dataset_id['aln_contigs'])
                 )
             )
         ])
        },
        {'tool' : tool_dict['domain_filter'],
         'inputs' : OrderedDict([
             ('gff', dataset(dataset_id['gff_dante']))
         ])
        },
        {'tool' : tool_dict['gff_to_tabular'],
         'inputs' : OrderedDict([
             ('gff', dataset(dataset_id['gff_dante']))
         ])
        },
        {'tool' : tool_dict['gff_extract'],
         'inputs' : OrderedDict([
             ('input_dna', dataset(dataset_id['gepy_genome'])),
             ('domains_gff', dataset(dataset_id['gff_dante']))
         ])
        },
        {'tool' : tool_dict['gff_summary'],
         'inputs' : OrderedDict([
             ('group', "Name"),
             ('inputgff', dataset(dataset_id['gff_dante']))
         ])
        }

    ]

    runs = affixer_runs + filtering_runs + dante_runs + various_utils
    return runs

def get_args():
    parser = argparse.ArgumentParser(description="Upload data to galaxy instance and perform tests",
                                     epilog="api key and galaxy url can be provided in credentials.py file")
    parser.add_argument("-k", "--key", type=str)
    parser.add_argument("-g", "--galaxy_url", type=str)
    args = parser.parse_args()
    if not args.key:
        from credentials import my_key
        args.key = my_key
    if not args.galaxy_url:
        from credentials import url
        args.galaxy_url = url
    return args

def main():
    args = get_args()
    gi = GalaxyInstance(args.galaxy_url, args.key)
    dataset_id, h1 = add_files_to_new_history(gi, files_to_upload)
    runs = create_run_definition(dataset_id, tools)

    result_id = []
    for r in runs:
        result = gi.tools.run_tool(
            history_id=h1['id'],
            tool_id=r['tool'],
            tool_inputs=make_inputs(r['inputs'])
        )
        result_id += [i['id'] for i in result['outputs']]
        # wait between submited jobs?
        time.sleep(30)

    # wait for runs to finish and repost status
    while True:
        running_job = 0
        ok_job = 0
        new_job = 0
        error_job = 0
        queued_job = 0
        for i in result_id + list(dataset_id.values()):
            ## TODO - check fo SQL errors
            result = gi.datasets.show_dataset(i)
            if result['state'] == 'new':
                new_job += 1
            if result['state'] == 'ok':
                ok_job += 1
            if result['state'] == 'error':
                error_job += 1
            if result['state'] == 'running':
                running_job += 1
            if result['state'] == 'queued':
                running_job += 1
        print("--------------------------")
        print(("new    : {}\n"
               "queued : {}\n"
               "running: {}\n"
               "ok     : {}\n"
               "error  : {}\n"
               "".format(new_job, queued_job, running_job, ok_job, error_job)
        ))
        if (running_job + new_job + queued_job) == 0:
            break
        time.sleep(10)

    for i in result_id + list(dataset_id.values()):
        result = gi.datasets.show_dataset(i)
        print("--------------------------")
        print("Job name    :", result['name'])
        print("Job state  :", result['state'])
        print("Output peak  :\n", result['peek'])

    print("--------------------------")
    print(("new    : {}\n"
           "queued : {}\n"
           "running: {}\n"
           "ok     : {}\n"
           "error  : {}\n"
           "".format(new_job, queued_job, running_job, ok_job, error_job)
    ))


if __name__ == "__main__":
    main()

