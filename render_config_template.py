#######################################################################################
#
#  Name: render_config_template.py
#
#  Objective:  The purpose of this script is to generate text files with complete
#              configurations for Catalyst 9300's to be deployed in Totowa IDF's.
#              The script loads in a single Jinja2 template , and IDF specific data
#              to populate the template in YAML.  The script generates a config for each
#              IDF.
#
#######################################################################################

from jinja2 import Environment, FileSystemLoader
import yaml


environment_path = "."
config_template_file_name = "" #"Totowa-C9300ConfigTemplate.j2"
#commandset_template_file_name = "Totowa-C9300CommandTemplate.j2"
commandset_template_file_name = "C9200-AL-Template.j2"
data_file_name = "XV-9200L-IDF18-BFL-SWA.yml"
#######################################################################################
#
# Name: Main
#
# Description:  Script entry point
#
# Arguments: None
#
# Return: None
#
#######################################################################################


def main():

    # We need jinja2 to load its necessary components.
    j2_environment = Environment(loader=FileSystemLoader(environment_path), trim_blocks=True, lstrip_blocks=True)

    # if that fails, let the user know, and raise an exception to fail the script
    if j2_environment is None:
        print("Unable to create jinja2 environment object.")
        raise

    # Iterate over the total number of IDF's to configure.  Using one single template,
    # a data file for each, individual configs are generated for each IDF
    # The filename of the generated config is the hostname of the idf in .txt format
    #for idf in range(0, idf_count):
        # idf+1 to correct for offset counter
        # expected filenname format: "Totowa-C9300-IDF{{x}}.yml" where {{x}} is the IDF number
        # e.g. Totowa-C9300-IDF1.yml
    #    data_file_name = f"Totowa-C9300-IDF{idf+1}.yml"
    with open(data_file_name) as config_handler:
        config_yaml = yaml.safe_load(config_handler)
        print(config_yaml)
        # render_config(config_yaml, j2_environment)
        render_commandset(config_yaml, j2_environment)

#######################################################################################
#
# Name: render_config
#
# Description:  Generates a configuration text file in the local path for a Catalyst 9300
#               access layer switch for Totowa.  A jinja2 template is populated using
#               IDF-specific data in YAML format.
#
# Arguments:
#               cfg_yml: yaml object with config data pre-loaded
#               env: Jinja2 environment variable used to populate template with data,
#                    and render the config
#
# Return: None
#
#######################################################################################


def render_config(cfg_yml, env):
    # load the template
    template = env.get_template(config_template_file_name)
    # render the IDF config using the template and the IDF-specific data
    rendered_config = template.render(**cfg_yml)

    # create the output file name for the specific IDF
    output_file_name = cfg_yml['Hostname'] + ".txt"

    # open, or create, that file, save the rendered config
    with open(f"{cfg_yml['Hostname']}-config.txt", "w") as output_handler:
        output_handler.write(rendered_config)

    print(f'Config rendered and saved to {output_file_name}')

#######################################################################################
#
# Name: render_config
#
# Description:  Generates a configuration text file in the local pathfor a Catalyst 9300
#               access layer switch for Totowa.  A jinja2 template is populated using
#               IDF-specific data in YAML format.
#
# Arguments:
#               cfg_yml: yaml object with config data pre-loaded
#               env: Jinja2 environment variable used to populate template with data,
#                    and render the config
#
# Return: None
#
#######################################################################################


def render_commandset(cmd_yml, env):
    # load the template
    template = env.get_template(commandset_template_file_name)
    # render the IDF config using the template and the IDF-specific data
    rendered_commandset = template.render(**cmd_yml)

    # create the output file name for the specific IDF
    output_file_name = f"{cmd_yml['Hostname']}-commandset.txt"

    # open, or create, that file, save the rendered config
    with open(output_file_name, "w") as output_handler:
        output_handler.write(rendered_commandset)

    print(f'Config rendered and saved to {output_file_name}')

#######################################################################################

# Force script to execute main() first

#######################################################################################


if __name__ == '__main__':
    main()

