from Utils import *
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser("HW1\n ")
    parser.add_argument("-f", '--input_file', help="path to DNA input file", required=True)
    parser.add_argument("-k", "--kmer", help="k-mer size")
    parser.add_argument("-m", "--mutation", help="mutation seq, capital letter no space(ex:AACCTT)",required=False)

    args = parser.parse_args()
    if args.input_file:
        read_dna_from_file(args.input_file)
    else:
        print("Provide input file!!")
    # k-mer size
    k = int(args.kmer)
    mutation_base = list(args.mutation)
    result_dict = {}
    for i in range(0,10):
        # apply mutation
        for seq_number in range(len(dna_strings) - 1):
            temp_mutation = get_random_mutation(copy.deepcopy(mutation_base), random.randint(0,4))
            dna_strings[seq_number] = apply_mutation(temp_mutation, dna_strings[seq_number])
        min_score = 500
        count = 0
        iter_count = 0
        # create motif matrix
        motif_matrix = get_motif_matrix(k, dna_strings)
        while count < 100:

            # drop gibb idx
            gibb_pass_idx = random.randint(0, len(dna_strings) - 1)
            motif_matrix.pop(gibb_pass_idx)

            # create profile
            profile_dict = get_profile(motif_matrix)

            [print(key,value) for key,value in profile_dict.items()]

            # apply pseudo count
            p_profile = apply_pseudo_count(profile_dict)

            # olasılık hesabı
            new_motif = get_new_motif_with_prob(k, dna_strings[gibb_pass_idx],p_profile)
            motif_matrix.insert(gibb_pass_idx, list(new_motif))
            # score calc
            score = get_score(k, profile_dict.values())
            print(f"Current Score: {score}")
            print(f"Minimum Score: {min_score}")
            iter_count = iter_count +1
            if min_score > score:
                min_score = score
                min_profile = profile_dict
                min_motif = motif_matrix
                count = 0
            else:
                count = count + 1

        print("Minimum profile:")
        [print(key,value) for key,value in min_profile.items()]
        print(f"Consensus String:{get_consensus_string(k,min_profile)}")
        print(f"Inserted mutation:{''.join(mutation_base)}")
        #print(f"number of iteration:{iter_count}")

        result_dict[i] ="Consensus string:" + str(get_consensus_string(k, min_profile)) + " number of iteration " + str(iter_count) + " Min score:"+str(min_score) + "\n" +str(["".join(seq) for seq in min_motif])
    [print(f"Iter {key} : {value}") for key,value in result_dict.items()]