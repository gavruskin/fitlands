import os.path
import sys
from three_way_epistasis import get_next_ordering, ordering_to_fitness, epistasis_positive, epistasis_negative
from circuit_epistasis import get_repetitions_from_circuit_number, get_positives_list, get_negatives_list

__author__ = "@gavruskin"


# Given a partial order in the form of adjacency lists, return all total extensions.
# Loops through all total orders looking for compatible ones.
def all_total_extensions_brute_force(graph):
    output = []
    ordering = [1, 1, 1, 1, 1, 1, 1, 1]
    fitness = [1, 2, 3, 4, 5, 6, 7, 8]
    compatible = True
    for edge in graph:
        if fitness.index(edge[0]) < fitness.index(edge[1]):
            compatible = False
            break
    if compatible:
        output.append(fitness)
    while ordering != [8, 7, 6, 5, 4, 3, 2, 1]:
        ordering = get_next_ordering(ordering)
        fitness = ordering_to_fitness(ordering)
        compatible = True
        for edge in graph:
            if fitness.index(edge[0]) < fitness.index(edge[1]):
                compatible = False
                break
        if compatible:
            output.append(fitness)
    return output


def genotype_to_index(genotype):
    if genotype == 0:
        return 1
    elif genotype == 1:
        return 2
    elif genotype == 10:
        return 3
    elif genotype == 100:
        return 4
    elif genotype == 11:
        return 5
    elif genotype == 101:
        return 6
    elif genotype == 110:
        return 7
    elif genotype == 111:
        return 8
    else:
        print("\ngenotype_to_index received a non-genotype as input")
        sys.exit()


# Returns a list of partial orders on the set {1, ..., 8} given a file with partial orders on the set {000, ..., 111}.
# The convention is: 000 = 1, 001 = 2, 010 = 3, 100 = 4, 011 = 5, 101 = 6, 110 = 7, 111 = 8
# (To be compatible with other functions.)
def partial_orders_from_file(file_name):
    if not os.path.isfile("./outputs/%s" % file_name):
        print("\nPlease put the file with partial orders into directory 'outputs' inside the working directory.\n"
              "Then, check that the script is called with the correctly spelled file name, including the extension.")
        sys.exit()
    partial_orders_file = open("./outputs/%s" % file_name, "r")
    output = []
    for line in partial_orders_file:
        if line != "\n":
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.replace(" ", "")
            partial_order = [int(s) for s in line.split(",")]
            for i in range(len(partial_order)):
                partial_order[i] = genotype_to_index(partial_order[i])
            partial_order_formatted = []
            for i in range(0, len(partial_order), 2):
                partial_order_formatted.append([partial_order[i], partial_order[i + 1]])
            output.append(partial_order_formatted)
    partial_orders_file.close()
    return output


# Returns a string over {000, ..., 111} that corresponds to total_order (list) over {1, ..., 8} using
# 000 = 1, 001 = 2, 010 = 3, 100 = 4, 011 = 5, 101 = 6, 110 = 7, 111 = 8
def convert_to_genotype(total_order):
    output = []
    for rank in total_order:
        if rank == 1:
            output.append("000")
        elif rank == 2:
            output.append("001")
        elif rank == 3:
            output.append("010")
        elif rank == 4:
            output.append("100")
        elif rank == 5:
            output.append("011")
        elif rank == 6:
            output.append("101")
        elif rank == 7:
            output.append("110")
        elif rank == 8:
            output.append("111")
    output = str(output)
    output = output.replace("'", "")
    return output


# Takes file ./outputs/partial_orders.md with partial orders.
# If 'details' == True, returns two files: ./outputs/partial_orders_analysis.md and
# ./outputs/partial_orders_analysis_details.md.
# The first one contains the number of total extensions of each of the partial orders with numbers and fractions of
# total orders that imply three-way epistasis.
# The second contains the lists of those orders. Takes more time to produce than only the numbers.
# If 'details' == False, only the first file is returned. More efficient.
def analyze_partial_orders(file_name, details=False):
    partial_orders = partial_orders_from_file(file_name)
    if os.path.isfile("./outputs/partial_orders_analysis.md"):
        print("\nFile partial_orders_analysis.md already exists in directory 'outputs'. Please remove and rerun.")
        sys.exit()
    output_file = open("./outputs/partial_orders_analysis.md", "w")
    output_file.write("This file has been created using software package Fitlands "
                      "(Alex Gavryushkin, CBG, D-BSSE, ETH Zurich).\n"
                      "Please refer to [https://github.com/gavruskin/fitlands] for legal matters, "
                      "to obtain up-to-date bibliographic information for Fitlands, "
                      "and to stay tuned.\n"
                      "If you publish the results obtained with the help of this software, "
                      "please don't forget to cite us.\n")
    if details:
        if os.path.isfile("./outputs/partial_orders_analysis_details.md"):
            print("\nFile partial_orders_analysis_details.md already exists in directory 'outputs'."
                  "Please remove and rerun.")
            sys.exit()
        output_file_details = open("./outputs/partial_orders_analysis_details.md", "w")
        output_file_details.write("This file has been created using software package Fitlands "
                                  "(Alex Gavryushkin, CBG, D-BSSE, ETH Zurich).\n"
                                  "Please refer to [https://github.com/gavruskin/fitlands] for legal matters, "
                                  "to obtain up-to-date bibliographic information for Fitlands, "
                                  "and to stay tuned.\n"
                                  "If you publish the results obtained with the help of this software, "
                                  "please don't forget to cite us.\n")
    for partial_order in partial_orders:
        partial_order_number = partial_orders.index(partial_order) + 1
        output_file.write("\n\n## Analysis of partial order number " + str(partial_order_number) + "\n\n")
        if details:
            output_file_details.write("\n\n## Analysis of partial order number " + str(partial_order_number) + "\n\n")
        total_extensions = all_total_extensions_brute_force(partial_order)
        imply_positive = []
        imply_negative = []
        for total_extension in total_extensions:
            if epistasis_positive(total_extension, positives={1, 5, 6, 7}, negatives={4, 3, 2, 8},
                                  repetitions=[1, 1, 1, 1, 1, 1, 1, 1]):
                imply_positive.append(total_extension)
            elif epistasis_negative(total_extension, positives={1, 5, 6, 7}, negatives={4, 3, 2, 8},
                                    repetitions=[1, 1, 1, 1, 1, 1, 1, 1]):
                imply_negative.append(total_extension)
        imply_epistasis_total = len(imply_positive) + len(imply_negative)
        imply_epistasis_total_percent = 100 * imply_epistasis_total / float(len(total_extensions))
        imply_positive_percent = 100 * len(imply_positive) / float(len(total_extensions))
        imply_negative_percent = 100 * len(imply_negative) / float(len(total_extensions))
        output_file.write("Number of total extensions: " + str(len(total_extensions)) + "\n" +
                          "Imply three-way interaction: " + str(imply_epistasis_total) +
                          " (%s%%)\n" % round(imply_epistasis_total_percent, 2) +
                          "Imply positive three-way interaction: " + str(len(imply_positive)) +
                          " (%s%%)\n" % round(imply_positive_percent, 2) +
                          "Imply negative three-way interaction: " + str(len(imply_negative)) +
                          " (%s%%)\n" % round(imply_negative_percent, 2))
        if details:
            output_file_details.write("Number of total extensions: " + str(len(total_extensions)) + "\n" +
                                      "Imply three-way interaction: " + str(imply_epistasis_total) +
                                      " (%s%%)\n" % round(imply_epistasis_total_percent, 2) +
                                      "Imply positive three-way interaction: " + str(len(imply_positive)) +
                                      " (%s%%)\n" % round(imply_positive_percent, 2) +
                                      "Imply negative three-way interaction: " + str(len(imply_negative)) +
                                      " (%s%%)\n" % round(imply_negative_percent, 2) + "\n" +
                                      "List of total extensions followed by three-way interaction signs:\n\n")
            for total_extension in total_extensions:
                output_file_details.write(convert_to_genotype(total_extension))
                if epistasis_positive(total_extension, positives={1, 5, 6, 7}, negatives={4, 3, 2, 8},
                                      repetitions=[1, 1, 1, 1, 1, 1, 1, 1]):
                    output_file_details.write("  +\n")
                elif epistasis_negative(total_extension, positives={1, 5, 6, 7}, negatives={4, 3, 2, 8},
                                        repetitions=[1, 1, 1, 1, 1, 1, 1, 1]):
                    output_file_details.write("  -\n")
                else:
                    output_file_details.write(" +/-\n")
    output_file.write("\n")
    output_file.close()
    if details:
        output_file_details.write("\n")
        output_file_details.close()
    return


# Creates a nice formula for the output file:
def get_circuit_formula(positives, negatives, repetitions):
    circuit = ""
    if 1 in positives:
        if repetitions[0] > 1:
            circuit += "%sw(000) " % str(repetitions[0])
        elif repetitions[0] == 1:
            circuit += "w(000) "
    elif 1 in negatives:
        if repetitions[0] > 1:
            circuit += "-%sw(000) " % str(repetitions[0])
        elif repetitions[0] == 1:
            circuit += "-w(000) "
    if 2 in positives:
        if repetitions[1] > 1:
            circuit += "+ %sw(001) " % str(repetitions[1])
        elif repetitions[1] == 1:
            circuit += "+ w(001) "
    elif 2 in negatives:
        if repetitions[1] > 1:
            circuit += "- %sw(001) " % str(repetitions[1])
        elif repetitions[1] == 1:
            circuit += "- w(001) "
    if 3 in positives:
        if repetitions[2] > 1:
            circuit += "+ %sw(010) " % str(repetitions[2])
        elif repetitions[2] == 1:
            circuit += "+ w(010) "
    elif 3 in negatives:
        if repetitions[2] > 1:
            circuit += "- %sw(010) " % str(repetitions[2])
        elif repetitions[2] == 1:
            circuit += "- w(010) "
    if 4 in positives:
        if repetitions[3] > 1:
            circuit += "+ %sw(100) " % repetitions[3]
        elif repetitions[3] == 1:
            circuit += "+ w(100) "
    elif 4 in negatives:
        if repetitions[3] > 1:
            circuit += "- %sw(100) " % repetitions[3]
        elif repetitions[3] == 1:
            circuit += "- w(100) "
    if 5 in positives:
        if repetitions[4] > 1:
            circuit += "+ %sw(011) " % repetitions[4]
        elif repetitions[4] == 1:
            circuit += "+ w(011) "
    elif 5 in negatives:
        if repetitions[4] > 1:
            circuit += "- %sw(011) " % repetitions[4]
        elif repetitions[4] == 1:
            circuit += "- w(011) "
    if 6 in positives:
        if repetitions[5] > 1:
            circuit += "+ %sw(101) " % repetitions[5]
        elif repetitions[5] == 1:
            circuit += "+ w(101) "
    elif 6 in negatives:
        if repetitions[5] > 1:
            circuit += "- %sw(101) " % repetitions[5]
        elif repetitions[5] == 1:
            circuit += "- w(101) "
    if 7 in positives:
        if repetitions[6] > 1:
            circuit += "+ %sw(110) " % repetitions[6]
        elif repetitions[6] == 1:
            circuit += "+ w(110) "
    elif 7 in negatives:
        if repetitions[6] > 1:
            circuit += "- %sw(110) " % repetitions[6]
        elif repetitions[6] == 1:
            circuit += "- w(110) "
    if 8 in positives:
        if repetitions[7] > 1:
            circuit += "+ %sw(111)" % repetitions[7]
        elif repetitions[7] == 1:
            circuit += "+ w(111)"
    elif 8 in negatives:
        if repetitions[7] > 1:
            circuit += "- %sw(111)" % repetitions[7]
        elif repetitions[7] == 1:
            circuit += "- w(111)"
    if circuit[1] == " ":
        circuit = circuit[0] + circuit[2:]
    if circuit[0] == "+":
        circuit = circuit[1:]
    while circuit[len(circuit) - 1] == " ":
        circuit = circuit[:len(circuit) - 1]
    return circuit


# Takes circuit as string in the format returned by get_circuit_formula and returns the name of the circuit
# as in BPS[2007].
def get_circuit_name(circuit):
    if circuit == "w(000) - w(001) - w(010) + w(100) + w(011) - w(101) - w(110) + w(111)":
        return "u(011)"
    elif circuit == "w(000) - w(001) + w(010) - w(100) - w(011) + w(101) - w(110) + w(111)":
        return "u(101)"
    elif circuit == "w(000) + w(001) - w(010) - w(100) - w(011) - w(101) + w(110) + w(111)":
        return "u(110)"
    elif circuit == "w(000) - w(001) - w(010) - w(100) + w(011) + w(101) + w(110) - w(111)":
        return "u(111)"
    elif circuit == "w(000) - w(010) - w(100) + w(110)":
        return "a"
    elif circuit == "w(001) - w(011) - w(101) + w(111)":
        return "b"
    elif circuit == "w(000) - w(001) - w(100) + w(101)":
        return "c"
    elif circuit == "w(010) - w(011) - w(110) + w(111)":
        return "d"
    elif circuit == "w(000) - w(001) - w(010) + w(011)":
        return "e"
    elif circuit == "w(100) - w(101) - w(110) + w(111)":
        return "f"
    elif circuit == "w(000) - w(100) - w(011) + w(111)":
        return "g"
    elif circuit == "w(001) - w(010) - w(101) + w(110)":
        return "h"
    elif circuit == "w(000) - w(010) - w(101) + w(111)":
        return "i"
    elif circuit == "w(001) - w(100) - w(011) + w(110)":
        return "j"
    elif circuit == "w(000) - w(001) - w(110) + w(111)":
        return "k"
    elif circuit == "w(010) - w(100) - w(011) + w(101)":
        return "l"
    elif circuit == "-2w(000) + w(001) + w(010) + w(100) - w(111)":
        return "m"
    elif circuit == "-w(000) + w(011) + w(101) + w(110) - 2w(111)":
        return "n"
    elif circuit == "-w(001) + w(010) + w(100) - 2w(110) + w(111)":
        return "o"
    elif circuit == "w(000) - 2w(001) + w(011) + w(101) - w(110)":
        return "p"
    elif circuit == "w(001) - w(010) + w(100) - 2w(101) + w(111)":
        return "q"
    elif circuit == "w(000) - 2w(010) + w(011) - w(101) + w(110)":
        return "r"
    elif circuit == "w(000) - 2w(100) - w(011) + w(101) + w(110)":
        return "s"
    elif circuit == "w(001) + w(010) - w(100) - 2w(011) + w(111)":
        return "t"
    else:
        return "Unknown circuit (error)"


# Takes circuit as a string in the format returned by get_circuit_formula and returns its biological meaning.
def get_circuit_meaning(circuit):
    if circuit == "w(000) - w(001) - w(010) + w(100) + w(011) - w(101) - w(110) + w(111)":
        return "marginal interaction between locus 2 and 3"
    elif circuit == "w(000) - w(001) + w(010) - w(100) - w(011) + w(101) - w(110) + w(111)":
        return "marginal interaction between locus 1 and 3"
    elif circuit == "w(000) + w(001) - w(010) - w(100) - w(011) - w(101) + w(110) + w(111)":
        return "marginal interaction between locus 1 and 2"
    elif circuit == "w(000) - w(001) - w(010) - w(100) + w(011) + w(101) + w(110) - w(111)":
        return "three-way interaction"
    elif circuit == "w(000) - w(010) - w(100) + w(110)":
        return "two-way interaction conditioned on locus 3 being 0"
    elif circuit == "w(001) - w(011) - w(101) + w(111)":
        return "two-way interaction conditioned on locus 3 being 1"
    elif circuit == "w(000) - w(001) - w(100) + w(101)":
        return "two-way interaction conditioned on locus 2 being 0"
    elif circuit == "w(010) - w(011) - w(110) + w(111)":
        return "two-way interaction conditioned on locus 2 being 1"
    elif circuit == "w(000) - w(001) - w(010) + w(011)":
        return "two-way interaction conditioned on locus 1 being 0"
    elif circuit == "w(100) - w(101) - w(110) + w(111)":
        return "two-way interaction conditioned on locus 1 being 1"
    elif circuit == "w(000) - w(100) - w(011) + w(111)":
        return "interaction between locus 1 and 2 conditioned on mutations at locus 2 and 3 coincide"
    elif circuit == "w(001) - w(010) - w(101) + w(110)":
        return "interaction between locus 1 and 2 conditioned on mutations at locus 2 and 3 are different"
    elif circuit == "w(000) - w(010) - w(101) + w(111)":
        return "interaction between locus 1 and 2 conditioned on mutations at locus 1 and 3 coincide"
    elif circuit == "w(001) - w(100) - w(011) + w(110)":
        return "interaction between locus 1 and 2 conditioned on mutations at locus 1 and 3 are different"
    elif circuit == "w(000) - w(001) - w(110) + w(111)":
        return "interaction between locus 1 and 3 conditioned on mutations at locus 1 and 2 coincide"
    elif circuit == "w(010) - w(100) - w(011) + w(101)":
        return "interaction between locus 1 and 3 conditioned on mutations at locus 1 and 2 are different"
    elif circuit == "-2w(000) + w(001) + w(010) + w(100) - w(111)":
        return "m"
    elif circuit == "-w(000) + w(011) + w(101) + w(110) - 2w(111)":
        return "n"
    elif circuit == "-w(001) + w(010) + w(100) - 2w(110) + w(111)":
        return "o"
    elif circuit == "w(000) - 2w(001) + w(011) + w(101) - w(110)":
        return "p"
    elif circuit == "w(001) - w(010) + w(100) - 2w(101) + w(111)":
        return "q"
    elif circuit == "w(000) - 2w(010) + w(011) - w(101) + w(110)":
        return "r"
    elif circuit == "w(000) - 2w(100) - w(011) + w(101) + w(110)":
        return "s"
    elif circuit == "w(001) + w(010) - w(100) - 2w(011) + w(111)":
        return "t"
    else:
        return "Unknown circuit (error)"


# Does the same things as analyze_partial_orders but with respect to the given circuit instead of the plain
# u_111 (three-way epistasis), which is the default option.
# Hence, with defaults the behavior is identical to analyze_partial_orders.
# If genotype_format is True (default), positives and negatives are taken in {0, 11, 101} format,
# otherwise---in index format: {1, 5, 6}.
#
# Example of usage:
# analyze_partial_orders_for_circuit("partial_orders.md", True, {0, 11}, {1, 10})
#
# The reason to keep both analyze_partial_orders and analyze_partial_orders_for_circuit is that the former should be
# more efficient, but that has to be tested.
def analyze_partial_orders_for_circuit(file_name, details=False,
                                       positives=None, negatives=None, repetitions=None, genotype_format=True):
    if repetitions is None:
        repetitions = [1, 1, 1, 1, 1, 1, 1, 1]
    else:
        repetitions[3], repetitions[4] = repetitions[4], repetitions[3]
    if positives is None:
        positives = {1, 5, 6, 7}
    elif genotype_format:
        positives = {genotype_to_index(i) for i in positives}
    if negatives is None:
        negatives = {4, 3, 2, 8}
    elif genotype_format:
        negatives = {genotype_to_index(i) for i in negatives}
    partial_orders = partial_orders_from_file(file_name)
    if os.path.isfile("./outputs/partial_orders_analysis.md"):
        print("\nFile partial_orders_analysis.md already exists in directory 'outputs'. Please remove and rerun.")
        sys.exit()
    output_file = open("./outputs/partial_orders_analysis.md", "w")
    output_file.write("This file has been created using software package Fitlands "
                      "(Alex Gavryushkin, CBG, D-BSSE, ETH Zurich).\n"
                      "Please refer to [https://github.com/gavruskin/fitlands] for legal matters, "
                      "to obtain up-to-date bibliographic information for Fitlands, "
                      "and to stay tuned.\n"
                      "If you publish the results obtained with the help of this software, "
                      "please don't forget to cite us.\n")
    circuit = get_circuit_formula(positives, negatives, repetitions)
    output_file.write("\n\n# Analysis of circuit interaction\ncircuit = " + circuit + "\n")
    if details:
        if os.path.isfile("./outputs/partial_orders_analysis_details.md"):
            print("\nFile partial_orders_analysis_details.md already exists in directory 'outputs'."
                  "Please remove and rerun.")
            sys.exit()
        output_file_details = open("./outputs/partial_orders_analysis_details.md", "w")
        output_file_details.write("This file has been created using software package Fitlands "
                                  "(Alex Gavryushkin, CBG, D-BSSE, ETH Zurich).\n"
                                  "Please refer to [https://github.com/gavruskin/fitlands] for legal matters, "
                                  "to obtain up-to-date bibliographic information for Fitlands, "
                                  "and to stay tuned.\n"
                                  "If you publish the results obtained with the help of this software, "
                                  "please don't forget to cite us.\n")
        output_file_details.write("\n\n# Analysis of circuit interaction\ncircuit = " + circuit + "\n")
    for partial_order in partial_orders:
        partial_order_number = partial_orders.index(partial_order) + 1
        output_file.write("\n\n## Analysis of partial order number " + str(partial_order_number) + "\n\n")
        if details:
            output_file_details.write("\n\n## Analysis of partial order number " + str(partial_order_number) + "\n\n")
        total_extensions = all_total_extensions_brute_force(partial_order)
        imply_positive = []
        imply_negative = []
        for total_extension in total_extensions:
            if epistasis_positive(total_extension, positives, negatives, repetitions):
                imply_positive.append(total_extension)
            elif epistasis_negative(total_extension, positives, negatives, repetitions):
                imply_negative.append(total_extension)
        imply_epistasis_total = len(imply_positive) + len(imply_negative)
        imply_epistasis_total_percent = 100 * imply_epistasis_total / float(len(total_extensions))
        imply_positive_percent = 100 * len(imply_positive) / float(len(total_extensions))
        imply_negative_percent = 100 * len(imply_negative) / float(len(total_extensions))
        output_file.write("Number of total extensions: " + str(len(total_extensions)) + "\n" +
                          "Imply circuit interaction: " + str(imply_epistasis_total) +
                          " (%s%%)\n" % round(imply_epistasis_total_percent, 2) +
                          "Imply positive circuit interaction: " + str(len(imply_positive)) +
                          " (%s%%)\n" % round(imply_positive_percent, 2) +
                          "Imply negative circuit interaction: " + str(len(imply_negative)) +
                          " (%s%%)\n" % round(imply_negative_percent, 2))
        if details:
            output_file_details.write("Number of total extensions: " + str(len(total_extensions)) + "\n" +
                                      "Imply circuit interaction: " + str(imply_epistasis_total) +
                                      " (%s%%)\n" % round(imply_epistasis_total_percent, 2) +
                                      "Imply positive circuit interaction: " + str(len(imply_positive)) +
                                      " (%s%%)\n" % round(imply_positive_percent, 2) +
                                      "Imply negative circuit interaction: " + str(len(imply_negative)) +
                                      " (%s%%)\n" % round(imply_negative_percent, 2) + "\n" +
                                      "List of total extensions followed by circuit interaction signs:\n\n")
            for total_extension in total_extensions:
                output_file_details.write(convert_to_genotype(total_extension))
                if epistasis_positive(total_extension, positives={1, 5, 6, 7}, negatives={4, 3, 2, 8},
                                      repetitions=[1, 1, 1, 1, 1, 1, 1, 1]):
                    output_file_details.write("  +\n")
                elif epistasis_negative(total_extension, positives={1, 5, 6, 7}, negatives={4, 3, 2, 8},
                                        repetitions=[1, 1, 1, 1, 1, 1, 1, 1]):
                    output_file_details.write("  -\n")
                else:
                    output_file_details.write(" +/-\n")
    output_file.write("\n")
    output_file.close()
    if details:
        output_file_details.write("\n")
        output_file_details.close()
    return


# Takes total_order as an input in the genotype format, e.g. {0, 11, 101} if genotype_format == True, or
# in index format, e.g. {1, 5, 6}, otherwise.
# Returns a file with the analysis of interactions implied by the rank order total_order for all 20 circuits.
def analyze_total_order_for_all_circuits(total_order, genotype_format=True):
    if genotype_format:
        total_order = [genotype_to_index(i) for i in total_order]
    if os.path.isfile("./outputs/total_order_analysis_for_all_circuits.md"):
        print("\nFile total_orders_analysis.md already exists in directory 'outputs'. Please remove and rerun.")
        sys.exit()
    output_file = open("./outputs/total_order_analysis_for_all_circuits.md", "w")
    output_file.write("This file has been created using software package Fitlands "
                      "(Alex Gavryushkin, CBG, D-BSSE, ETH Zurich).\n"
                      "Please refer to [https://github.com/gavruskin/fitlands] for legal matters, "
                      "to obtain up-to-date bibliographic information for Fitlands, "
                      "and to stay tuned.\n"
                      "If you publish the results obtained with the help of this software, "
                      "please don't forget to cite us.\n")

    positives_list = get_positives_list()  # These lists include circuits and interaction coordinates.
    negatives_list = get_negatives_list()
    imply_positive = []  # Compute circuit interaction.
    imply_negative = []
    circuits = []
    for circuit_number in range(20):
        positives = positives_list[circuit_number]
        negatives = negatives_list[circuit_number]
        repetitions = get_repetitions_from_circuit_number(circuit_number + 1)
        circuit = get_circuit_formula(positives, negatives, repetitions)
        circuits.append(circuit)
        if epistasis_positive(total_order, positives, negatives, repetitions):
            imply_positive.append(circuit)
        elif epistasis_negative(total_order, positives, negatives, repetitions):
            imply_negative.append(circuit)
    interaction_total = len(imply_positive) + len(imply_negative)
    interaction_percent = 100 * interaction_total / float(20)
    imply_positive_percent = 100 * len(imply_positive) / float(20)
    imply_negative_percent = 100 * len(imply_negative) / float(20)

    imply_positive_interaction_coordinates = []  # Compute interaction implied by interaction coordinates.
    imply_negative_interaction_coordinates = []
    circuits_interaction_coordinates = []
    for circuit_number in range(20, 24):
        positives = positives_list[circuit_number]
        negatives = negatives_list[circuit_number]
        repetitions = get_repetitions_from_circuit_number(circuit_number + 1)
        circuit = get_circuit_formula(positives, negatives, repetitions)
        circuits_interaction_coordinates.append(circuit)
        if epistasis_positive(total_order, positives, negatives, repetitions):
            imply_positive_interaction_coordinates.append(circuit)
        elif epistasis_negative(total_order, positives, negatives, repetitions):
            imply_negative_interaction_coordinates.append(circuit)

    # Write the results into the file.
    output_file.write("\n\n# Analysis of interaction coordinates and circuit interactions\n"
                      "The three-way interaction corresponds to the last interaction coordinate u(111)\n\n"
                      "Rank order: %s\n" % convert_to_genotype(total_order))

    # Write the result of interaction coordinate analysis into the file.
    output_file.write("\n\n## Interaction coordinates\n\n")
    for circuit in circuits_interaction_coordinates:
        if circuit in imply_positive_interaction_coordinates:
            output_file.write("{0} = {1} implies positive interaction\n".format(get_circuit_name(circuit), circuit))
        elif circuit in imply_negative_interaction_coordinates:
            output_file.write("{0} = {1} implies negative interaction\n".format(get_circuit_name(circuit), circuit))
        else:
            output_file.write("{0} = {1} does not imply interaction\n".format(get_circuit_name(circuit), circuit))

    # Write the result of circuit interaction analysis into the file.
    output_file.write("\n\n## Circuits\n\n")
    output_file.write("The number of circuits for which the rank order implies circuit interaction: %s (%s%%)\n"
                      % (interaction_total, round(interaction_percent, 2)))
    output_file.write("The number of circuits for which the rank order implies *positive* circuit interaction: "
                      "%s (%s%%)\n"
                      % (len(imply_positive), round(imply_positive_percent, 2)))
    output_file.write("The number of circuits for which the rank order implies *negative* circuit interaction: "
                      "%s (%s%%)\n"
                      % (len(imply_negative), round(imply_negative_percent, 2)))
    output_file.write("\n\n### List of circuits for which the rank order implies *positive* interaction\n\n")
    for circuit in imply_positive:
        output_file.write("{0} = {1}\n".format(get_circuit_name(circuit), circuit))
    output_file.write("\n\n### List of circuits for which the rank order implies *negative* interaction\n\n")
    for circuit in imply_negative:
        output_file.write("{0} = {1}\n".format(get_circuit_name(circuit), circuit))
    output_file.write("\n\n### List of circuits followed by the interaction sign implied by the rank order\n\n"
                      "Circuit | Interaction sign\n"
                      "--- | ---\n")
    for circuit in circuits:
        if circuit in imply_positive:
            output_file.write("{0} = {1} | +\n".format(get_circuit_name(circuit), circuit))
        elif circuit in imply_negative:
            output_file.write("{0} = {1} | -\n".format(get_circuit_name(circuit), circuit))
        else:
            output_file.write("{0} = {1} | +/-\n".format(get_circuit_name(circuit), circuit))
    output_file.close()
    return
