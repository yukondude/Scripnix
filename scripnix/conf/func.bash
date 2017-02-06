# Common function definitions. Do not edit these. Instead, override values as needed in /etc/scripnix/conf.bash or ~/.scripnix/conf.bash.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.


# Exit with error message if the count of command arguments does not fall into
# the expected range. Use -1 to indicate no minimum/maximum.
# Example call: check_arg_count ${0} ${#} 2 2 '<arg1> <arg2>' ${1}
check_arg_count() {
    # Parameters:
    command=${1}
    arg_count=${2}
    min_count=${3}
    max_count=${4}
    usage=${5}
    first=${6}

    if [[ ${max_count} -lt 0 ]] ; then
        max_count=9999 # infinity!
    fi

    gsed=$(gnu_equivalent 'sed')

    if [[ -n ${first} ]] ; then
        if [[ ${first} == '-h' || ${first} == '--help' ]] ; then
            echo "Usage:" $(basename ${command}) "${usage}"
            echo
            $gsed --quiet --regexp-extended --expression '3,/^$/p' "${command}" | $gsed 's/^# /  /'
            echo "  The $(basename ${command}) command is part of Scripnix."
            exit 0
        fi
    fi

    if [[ ${arg_count} -lt ${min_count} || ${arg_count} -gt ${max_count} ]] ; then
        echo_err "Usage:" $(basename ${command}) "${usage}"
        exit 1
    fi
}


# Collect switches from a file and return as a single space-delimited string
# (with redundant spaces stripped).
collect_switches() {
    switch_file="${1}"
    if [[ ! -f "${switch_file}" ]] ; then exit 0 ; fi
    cat "${switch_file}" |
        tr '\n' ' ' |
        sed --expression 's/  +/ /g' --regexp-extended
}


# Echo to standard error.
echo_err() {
    echo "$*" >&2
}


# Echo backslash-escaped forward-slashes.
escape_slashes() {
    echo "$*" | sed 's/\//\\\//g'
}


# Exclude common version control subdirectories.
exclude-vc() {
    egrep --invert-match '(\.hg|\.git|\.svn)\/'
}


# Return the gnu-equivalent command for MacOS, if it exists.
gnu_equivalent() {
    command=${1}
    gnu_command="g${command}"

    if [[ $(os-name) == 'macos' ]] ; then
        if hash "${gnu_command}" >/dev/null 2>&1 ; then
            command="${gnu_command}"
        fi
    fi

    echo "${command}"
}


# Exit with error if not the root user.
require_root() {
    if [ $(id -u) -ne 0 ] ; then
        echo_err "You must be root to execute this command. Try running it as: sudo" $(basename ${0})
        exit 2
    fi
}
