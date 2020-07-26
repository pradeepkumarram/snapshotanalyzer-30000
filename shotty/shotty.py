import boto3
import click

session = boto3.Session(profile_name='snapshot')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


@click.group()
def cli():
    "Managing snapshots"

@cli.group('volumes')
def volumes():
    """ Commands for Volumes """

@volumes.command('list')
@click.option('--project', default=None, help='Only volumes for project (tag Project:<name>)')
def list_volumes(project):
    "List Volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + 'GiB',
                v.encrypted and 'Encrypted' or 'Non encrypted'
            ))
            )
    return

@cli.group('instances')
def instances():
    """ Commands for instances """

@instances.command('list')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no project>')
        ))
        )
    return

@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')
def stop_instance(project):
    "Stop EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}".format(i.id))
        i.stop()
    return


@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for Project')
def start_instances(project):
    "Start instances"
    instances = filter_instances(project)

    for i in instances:
        print('Starting instance {0}...'.format(i.id))
        i.start()

    return

if __name__ == '__main__':
        cli()
